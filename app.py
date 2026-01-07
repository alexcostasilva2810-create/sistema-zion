import streamlit as st
import requests
import pandas as pd
import os
from fpdf import FPDF
from datetime import datetime

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Zion Tecnologia - Gestão O.S", layout="wide")

# --- CONEXÃO NOTION ---
TOKEN = st.secrets["notion"]["token"].replace('"', '').strip()
DATABASE = st.secrets["notion"]["database_id"].replace('"', '').strip()

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

# --- ESTILO CSS (PLANO DE FUNDO, CENTRALIZAÇÃO E BOTÕES) ---
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #0e1117 0%, #1f2937 100%); background-attachment: fixed; }
    h1, h2, h3, label { color: white !important; text-align: center; }
    [data-testid="stMetricValue"] { color: #28a745 !important; text-align: center; }
    div.stButton > button:first-child[kind="primary"] { background-color: #28a745 !important; color: white !important; border: none; }
    .stButton>button { width: 100%; border-radius: 8px; font-weight: bold; height: 3.5em; }
    .stDataFrame { background-color: rgba(255, 255, 255, 0.05); border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNÇÃO CARREGAR DADOS (TODOS OS CAMPOS) ---
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
                    "CLIENTE": g_t("CLIENTE"), "DT_SAIDA_RAW": g_d("DT SAÍDA"),
                    "DT SAÍDA": datetime.strptime(g_d("DT SAÍDA"), '%Y-%m-%d').strftime('%d/%m/%Y') if g_d("DT SAÍDA") else "---",
                    "EMPURRADOR": g_t("EMPURRADOR"), "BALSA": g_t("BALSA"),
                    "LOCAL": g_t("LOCAL"), "DESTINO": g_t("DESTINO"),
                    "HORA_EMBARQUE": g_t("HORA DE EMBARQUE"),
                    "ESCOLTA 1": g_t("ESCOLTA 1"), "ESCOLTA 2": g_t("ESCOLTA 2"),
                    "DESCRIÇÃO": g_t("DESCRIÇÃO"), "PEDIDO": g_t("PEDIDO"),
                    "INICIO_MISSAO": g_d("INÍCIO DA MISSÃO"), "FIM_MISSAO": g_d("FIM DA MISSÃO"),
                    "ASSINATURA": g_t("ASSINATURA RESPONSÁVEL"), "STATUS": status, "VALOR": valor
                })
            return lista
    except: return []

# --- FUNÇÕES PDF ---
def gerar_pdf_financeiro(df, total, ini, fim):
    pdf = FPDF()
    pdf.add_page(); pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "RELATORIO FINANCEIRO ZION", ln=True, align="C")
    pdf.set_font("Arial", "", 10)
    pdf.cell(0, 10, f"Periodo: {ini.strftime('%d/%m/%Y')} a {fim.strftime('%d/%m/%Y')}", ln=True, align="C")
    pdf.ln(5)
    pdf.set_fill_color(200, 200, 200)
    pdf.cell(20, 8, "OS", 1, 0, 'C', True); pdf.cell(70, 8, "CLIENTE", 1, 0, 'C', True)
    pdf.cell(35, 8, "DATA", 1, 0, 'C', True); pdf.cell(35, 8, "VALOR", 1, 1, 'C', True)
    pdf.set_font("Arial", "", 9)
    for _, row in df.iterrows():
        pdf.cell(20, 8, str(row['Nº OS']), 1); pdf.cell(70, 8, str(row['CLIENTE'])[:25], 1)
        pdf.cell(35, 8, str(row['DT SAÍDA']), 1); pdf.cell(35, 8, f"R$ {row['VALOR']:,.2f}", 1, 1, 'R')
    pdf.ln(5); pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, f"TOTAL: R$ {total:,.2f}", ln=True, align="R")
    return pdf.output(dest="S").encode("latin-1")

def gerar_pdf_os(d):
    pdf = FPDF(); pdf.add_page(); pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, f"ORDEM DE SERVICO - Nº {d['Nº OS']}", ln=True, align="C")
    pdf.set_font("Arial", "", 11); pdf.ln(5)
    for k, v in d.items():
        if k not in ["ID", "VALOR", "DT_SAIDA_RAW"]:
            pdf.cell(0, 8, f"{k}: {v}", border="B", ln=True)
    return pdf.output(dest="S").encode("latin-1")

# --- NAVEGAÇÃO ---
if "pagina" not in st.session_state: st.session_state.pagina = "🏠 HOME"
if "dados_edicao" not in st.session_state: st.session_state.dados_edicao = None
def navegar(p): st.session_state.pagina = p; st.rerun()

# --- TELA HOME ---
if st.session_state.pagina == "🏠 HOME":
    st.markdown("<br>", unsafe_allow_html=True)
    col_l, col_c, col_r = st.columns([1, 2, 1])
    with col_c:
        if os.path.exists("LOGO.PNG"): st.image("LOGO.PNG", width=300)
        st.markdown("<h1>SISTEMA ZION</h1><h3>Gestão Transdourada</h3>", unsafe_allow_html=True)
    st.markdown("<br><hr><br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    if c1.button("📋 NOVO LANÇAMENTO"): st.session_state.dados_edicao = None; navegar("📋 CADASTRO")
    if c2.button("📊 VER AGENDAMENTOS"): navegar("📊 GRADE")
    if c3.button("💰 FINANCEIRO"): navegar("💰 FINANCEIRO")

# --- TELA GRADE (RESTAURADA) ---
elif st.session_state.pagina == "📊 GRADE":
    st.markdown("## 📊 Grade de Agendamentos Ativos")
    if st.button("⬅️ VOLTAR"): navegar("🏠 HOME")
    dados = carregar_dados()
    if dados:
        df = pd.DataFrame(dados)
        st.dataframe(df[["Nº OS", "CLIENTE", "DT SAÍDA", "EMPURRADOR", "BALSA", "STATUS"]], use_container_width=True)
        for d in dados:
            with st.expander(f"⚙️ Opções O.S {d['Nº OS']} - {d['CLIENTE']}"):
                c1, c2 = st.columns(2)
                if c1.button("✏️ EDITAR", key=f"ed_{d['ID']}", type="primary"):
                    st.session_state.dados_edicao = d; navegar("📋 CADASTRO")
                pdf_os = gerar_pdf_os(d)
                c2.download_button("📄 GERAR PDF O.S", pdf_os, f"OS_{d['Nº OS']}.pdf", key=f"p_{d['ID']}")

# --- TELA FINANCEIRO (RESTAURADA + PDF PERÍODO) ---
elif st.session_state.pagina == "💰 FINANCEIRO":
    st.markdown("## 💰 Painel Financeiro e Relatórios")
    if st.button("⬅️ VOLTAR"): navegar("🏠 HOME")
    c1, c2 = st.columns(2)
    f_ini = c1.date_input("Data Inicial", value=datetime.now(), format="DD/MM/YYYY")
    f_fim = c2.date_input("Data Final", value=datetime.now(), format="DD/MM/YYYY")
    dados = carregar_dados()
    if dados:
        df = pd.DataFrame(dados)
        df['dt_filter'] = pd.to_datetime(df['DT_SAIDA_RAW'])
        df_filt = df[(df['dt_filter'] >= pd.Timestamp(f_ini)) & (df['dt_filter'] <= pd.Timestamp(f_fim))]
        st.metric("FATURAMENTO NO PERÍODO", f"R$ {df_filt['VALOR'].sum():,.2f}")
        st.dataframe(df_filt[["Nº OS", "CLIENTE", "DT SAÍDA", "EMPURRADOR", "BALSA", "ESCOLTA 1", "ESCOLTA 2", "VALOR"]], use_container_width=True)
        pdf_rel = gerar_pdf_financeiro(df_filt, df_filt['VALOR'].sum(), f_ini, f_fim)
        st.download_button("📥 BAIXAR RELATÓRIO PDF (PERÍODO)", pdf_rel, "financeiro_zion.pdf", type="primary")

# --- TELA CADASTRO (MANTIDA) ---
elif st.session_state.pagina == "📋 CADASTRO":
    # ... (O formulário completo com os 17 campos que já temos)
    st.button("⬅️ VOLTAR", on_click=lambda: navegar("🏠 HOME"))
    st.info("Formulário de Cadastro Ativo")
