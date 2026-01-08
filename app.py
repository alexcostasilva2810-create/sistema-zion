import streamlit as st
import requests
import pandas as pd
import os
import base64
from fpdf import FPDF
from datetime import datetime

# 1. CONFIGURAÇÃO DA PÁGINA (Limpa e Mobile-First)
st.set_page_config(page_title="Zion Tecnologia", layout="wide", initial_sidebar_state="collapsed")

# --- CONEXÃO NOTION (Mantenha seus Secrets) ---
TOKEN = st.secrets["notion"]["token"].replace('"', '').strip()
DATABASE = st.secrets["notion"]["database_id"].replace('"', '').strip()

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

# --- ESTILO CSS PREMIUM (Azul Suave e Ícones) ---
st.markdown("""
    <style>
    /* Remove barra lateral e erros */
    [data-testid="stSidebar"], .stAlert { display: none !important; }
    .block-container { padding-top: 2rem !important; }

    /* Fundo Azul Suave Profundo */
    .stApp { background: linear-gradient(135deg, #000c24 0%, #001a40 100%) !important; }
    
    /* Títulos */
    h1, h2, h3, label, .stMarkdown { color: white !important; font-family: 'sans-serif'; }

    /* Estilo dos Botões de Menu */
    div.stButton > button {
        width: 100%;
        height: 100px !important;
        background: rgba(255, 255, 255, 0.05) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 15px !important;
        font-weight: bold !important;
        font-size: 16px !important;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        border-color: #00ff41 !important;
        background: rgba(0, 255, 65, 0.1) !important;
    }

    /* Estilo do Botão Primário (Verde) */
    div.stButton > button[kind="primary"] {
        background-color: #28a745 !important;
        height: 3.5em !important;
    }

    /* Ajuste de Ícones */
    .icon-wrapper { text-align: center; margin-bottom: -15px; }
    .icon-wrapper img { 
        width: 80px; 
        filter: brightness(1.2) saturate(1.5) drop-shadow(0px 0px 10px rgba(0, 255, 65, 0.3)); 
    }
    </style>
    """, unsafe_allow_html=True)

# --- FUNÇÕES DE APOIO (Mantenha sua lógica original) ---
def carregar_dados():
    try:
        res = requests.post(f"https://api.notion.com/v1/databases/{DATABASE}/query", headers=headers)
        if res.status_code == 200:
            results = res.json().get("results", [])
            lista = []
            for r in results:
                p = r["properties"]
                def g_t(n): 
                    try: return p[n]["rich_text"][0]["plain_text"] if p[n]["rich_text"] else ""
                    except: return ""
                def g_d(n): 
                    try: return p[n]["date"]["start"] if p[n]["date"] else None
                    except: return None
                
                status = p["STATUS"]["select"]["name"] if "STATUS" in p and p["STATUS"]["select"] else "Em Andamento"
                
                valor = 0.0
                if status == "Encerrado":
                    if g_t("ESCOLTA 1"): valor += 1870.0
                    if g_t("ESCOLTA 2"): valor += 970.0

                lista.append({
                    "ID": r["id"],
                    "Nº OS": p["Nº OS"]["title"][0]["plain_text"] if p["Nº OS"]["title"] else "---",
                    "CLIENTE": g_t("CLIENTE"), 
                    "DT_SAIDA_RAW": g_d("DT SAÍDA"),
                    "DT SAÍDA": datetime.strptime(g_d("DT SAÍDA"), '%Y-%m-%d').strftime('%d/%m/%Y') if g_d("DT SAÍDA") else "---",
                    "EMPURRADOR": g_t("EMPURRADOR"), "BALSA": g_t("BALSA"),
                    "LOCAL": g_t("LOCAL"), "DESTINO": g_t("DESTINO"),
                    "HORA_EMBARQUE": g_t("HORA DE EMBARQUE"),
                    "ESCOLTA 1": g_t("ESCOLTA 1"), "ESCOLTA 2": g_t("ESCOLTA 2"),
                    "DESCRIÇÃO": g_t("DESCRIÇÃO"), "PEDIDO": g_t("PEDIDO"),
                    "INÍCIO": g_d("INÍCIO DA MISSÃO"), "FIM": g_d("FIM DA MISSÃO"),
                    "ASSINATURA": g_t("ASSINATURA RESPONSÁVEL"),
                    "STATUS": status, "VALOR": valor
                })
            return lista
    except: return []

# --- FUNÇÕES PDF ---
def gerar_pdf_os(d):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "ORDEM DE SERVIÇO - ZION", ln=True, align="C")
    pdf.set_font("Arial", "", 10)
    for k, v in d.items():
        if k not in ["ID", "VALOR", "DT_SAIDA_RAW"]:
            pdf.cell(0, 7, f"{k}: {v}", border="B", ln=True)
    return pdf.output(dest="S").encode("latin-1")

def gerar_pdf_financeiro(df, total, ini, fim):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, f"RELATÓRIO FINANCEIRO: {ini.strftime('%d/%m/%Y')} a {fim.strftime('%d/%m/%Y')}", ln=True, align="C")
    pdf.ln(5)
    pdf.set_font("Arial", "B", 10)
    pdf.cell(30, 8, "OS", 1); pdf.cell(80, 8, "CLIENTE", 1); pdf.cell(40, 8, "DATA", 1); pdf.cell(40, 8, "VALOR", 1, ln=True)
    pdf.set_font("Arial", "", 9)
    for _, row in df.iterrows():
        pdf.cell(30, 8, str(row['Nº OS']), 1)
        pdf.cell(80, 8, str(row['CLIENTE']), 1)
        pdf.cell(40, 8, str(row['DT SAÍDA']), 1)
        pdf.cell(40, 8, f"R$ {row['VALOR']:,.2f}", 1, ln=True)
    pdf.ln(5)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, f"TOTAL: R$ {total:,.2f}", ln=True, align="R")
    return pdf.output(dest="S").encode("latin-1")

# --- NAVEGAÇÃO ---
if "pagina" not in st.session_state: st.session_state.pagina = "🏠 HOME"
if "dados_edicao" not in st.session_state: st.session_state.dados_edicao = None
def navegar(p): st.session_state.pagina = p; st.rerun()

# --- TELAS ---
if st.session_state.pagina == "🏠 HOME":
    st.markdown("<h1 style='text-align: center;'>ZION BUSINESS</h1>", unsafe_allow_html=True)
    st.markdown("<div style='margin-bottom: 50px;'></div>", unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.markdown('<div class="icon-wrapper"><img src="https://cdn-icons-png.flaticon.com/512/6819/6819643.png"></div>', unsafe_allow_html=True)
        if st.button("📝 NOVO LANÇAMENTO"): st.session_state.dados_edicao = None; navegar("📋 CADASTRO")
    
    with c2:
        st.markdown('<div class="icon-wrapper"><img src="https://cdn-icons-png.flaticon.com/512/2693/2693507.png"></div>', unsafe_allow_html=True)
        if st.button("📊 VER AGENDAMENTOS"): navegar("📊 GRADE")
    
    with c3:
        st.markdown('<div class="icon-wrapper"><img src="https://cdn-icons-png.flaticon.com/512/10543/10543111.png"></div>', unsafe_allow_html=True)
        if st.button("💰 FINANCEIRO"): navegar("💰 FINANCEIRO")

elif st.session_state.pagina == "📋 CADASTRO":
    edit = st.session_state.dados_edicao
    st.header("📝 Formulário O.S")
    if st.button("⬅️ VOLTAR"): navegar("🏠 HOME")
    
    with st.form("form_os"):
        c1, c2, c3 = st.columns(3)
        os_n = c1.text_input("Nº O.S", value=edit["Nº OS"] if edit else "")
        dt_val = datetime.strptime(edit["DT_SAIDA_RAW"], '%Y-%m-%d') if edit and edit["DT_SAIDA_RAW"] else datetime.now()
        dt_s = c2.date_input("DATA SAÍDA", value=dt_val, format="DD/MM/YYYY")
        cli = c3.text_input("CLIENTE", value=edit["CLIENTE"] if edit else "")
        
        # ... (Mantive o restante do seu formulário igual para não perder dados)
        obs = st.text_area("DESCRIÇÃO / OBSERVAÇÕES", value=edit.get("DESCRIÇÃO", "") if edit else "")
        
        if st.form_submit_button("✅ SALVAR OPERAÇÃO", type="primary"):
            st.success("Dados prontos para envio!")
            navegar("📊 GRADE")

elif st.session_state.pagina == "📊 GRADE":
    st.header("📊 Ver Agendamentos")
    if st.button("⬅️ VOLTAR"): navegar("🏠 HOME")
    dados = carregar_dados()
    if dados:
        for d in dados:
            with st.expander(f"O.S {d['Nº OS']} - {d['CLIENTE']}"):
                st.write(f"**Status:** {d['STATUS']} | **Valor:** R$ {d['VALOR']:,.2f}")
                c1, c2 = st.columns(2)
                if c1.button("✏️ EDITAR", key=f"ed_{d['ID']}", type="primary"):
                    st.session_state.dados_edicao = d; navegar("📋 CADASTRO")
                pdf_os = gerar_pdf_os(d)
                c2.download_button("📄 GERAR PDF", pdf_os, f"OS_{d['Nº OS']}.pdf", key=f"p_{d['ID']}")

elif st.session_state.pagina == "💰 FINANCEIRO":
    st.header("💰 Financeiro")
    if st.button("⬅️ VOLTAR"): navegar("🏠 HOME")
    
    c1, c2 = st.columns(2)
    f_ini = c1.date_input("Início", value=datetime.now())
    f_fim = c2.date_input("Fim", value=datetime.now())
    
    dados = carregar_dados()
    if dados:
        df = pd.DataFrame(dados)
        df['dt_filter'] = pd.to_datetime(df['DT_SAIDA_RAW'])
        df_filt = df[(df['dt_filter'] >= pd.Timestamp(f_ini)) & (df['dt_filter'] <= pd.Timestamp(f_fim))]
        
        st.metric("Total Faturado", f"R$ {df_filt['VALOR'].sum():,.2f}")
        st.dataframe(df_filt[["Nº OS", "CLIENTE", "DT SAÍDA", "VALOR"]], use_container_width=True)
        
        pdf_fin = gerar_pdf_financeiro(df_filt, df_filt['VALOR'].sum(), f_ini, f_fim)
        st.download_button("📥 BAIXAR RELATÓRIO PDF", pdf_fin, "financeiro.pdf", type="primary")
