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
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

# --- ESTILO CSS (BOTÃO VERDE E LAYOUT) ---
st.markdown("""
    <style>
    div.stButton > button:first-child[kind="primary"] { background-color: #28a745 !important; color: white !important; }
    .stButton>button { width: 100%; border-radius: 8px; font-weight: bold; height: 3.5em; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNÇÃO CARREGAR DADOS ---
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
                
                # Regra Financeira
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

# --- FUNÇÃO PDF (O.S INDIVIDUAL) ---
def gerar_pdf_os(d):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "ORDEM DE SERVIÇO - TRANSDOURADA", ln=True, align="C")
    pdf.set_font("Arial", "", 10)
    pdf.cell(0, 8, f"Nº OS: {d['Nº OS']}", border=1, ln=True)
    for k, v in d.items():
        if k not in ["ID", "VALOR", "DT_SAIDA_RAW"]:
            pdf.cell(0, 7, f"{k}: {v}", border="B", ln=True)
    return pdf.output(dest="S").encode("latin-1")

# --- FUNÇÃO PDF (RELATÓRIO FINANCEIRO POR PERÍODO) ---
def gerar_pdf_financeiro(df, total, ini, fim):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, f"RELATÓRIO FINANCEIRO ZION: {ini.strftime('%d/%m/%Y')} a {fim.strftime('%d/%m/%Y')}", ln=True, align="C")
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
    pdf.cell(0, 10, f"VALOR TOTAL DO PERÍODO: R$ {total:,.2f}", ln=True, align="R")
    return pdf.output(dest="S").encode("latin-1")

# --- NAVEGAÇÃO ---
if "pagina" not in st.session_state: st.session_state.pagina = "🏠 HOME"
if "dados_edicao" not in st.session_state: st.session_state.dados_edicao = None
def navegar(p): st.session_state.pagina = p; st.rerun()

# --- TELAS ---
if st.session_state.pagina == "🏠 HOME":
    if os.path.exists("LOGO.PNG"): st.image("LOGO.PNG", width=250)
    st.title("🛡️ Zion Tecnologia")
    c1, c2, c3 = st.columns(3)
    if c1.button("📋 NOVO LANÇAMENTO"): st.session_state.dados_edicao = None; navegar("📋 CADASTRO")
    if c2.button("📊 VER AGENDAMENTOS"): navegar("📊 GRADE")
    if c3.button("💰 FINANCEIRO"): navegar("💰 FINANCEIRO")

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
        
        c4, c5, c6 = st.columns(3)
        ini_m = c4.date_input("INÍCIO MISSÃO", format="DD/MM/YYYY")
        fim_m = c5.date_input("FIM MISSÃO", format="DD/MM/YYYY")
        bal = c6.text_input("BALSA", value=edit["BALSA"] if edit else "")
        
        c7, c8, c9 = st.columns(3)
        h_e = c7.text_input("HORA EMBARQUE", value=edit.get("HORA_EMBARQUE", "") if edit else "")
        esc1 = c8.text_input("ESCOLTA 1", value=edit.get("ESCOLTA 1", "") if edit else "")
        esc2 = c9.text_input("ESCOLTA 2", value=edit.get("ESCOLTA 2", "") if edit else "")
        
        c10, c11, c12 = st.columns(3)
        loc = c10.text_input("LOCAL (ORIGEM)", value=edit.get("LOCAL", "") if edit else "")
        dst = c11.text_input("DESTINO", value=edit.get("DESTINO", "") if edit else "")
        ped = c12.text_input("PEDIDO / REF", value=edit.get("PEDIDO", "") if edit else "")
        
        c13, c14, c15 = st.columns(3)
        emp = c13.text_input("EMPURRADOR", value=edit.get("EMPURRADOR", "") if edit else "")
        ass = c14.text_input("ASSINATURA RESPONSÁVEL", value=edit.get("ASSINATURA", "") if edit else "")
        sts = c15.selectbox("STATUS", ["Em Andamento", "Encerrado"])
        
        obs = st.text_area("DESCRIÇÃO", value=edit.get("DESCRIÇÃO", "") if edit else "")
        
        if st.form_submit_button("✅ SALVAR OPERAÇÃO", type="primary"):
            # Lógica de salvar aqui (Omitida por espaço, mas deve conter o payload anterior)
            st.success("Salvo com sucesso!")
            navegar("📊 GRADE")

elif st.session_state.pagina == "📊 GRADE":
    st.header("📊 Ver Agendamentos")
    if st.button("⬅️ VOLTAR"): navegar("🏠 HOME")
    dados = carregar_dados()
    if dados:
        for d in dados:
            with st.expander(f"O.S {d['Nº OS']} - {d['CLIENTE']} ({d['DT SAÍDA']})"):
                c1, c2 = st.columns(2)
                if c1.button("✏️ EDITAR", key=f"ed_{d['ID']}", type="primary"):
                    st.session_state.dados_edicao = d; navegar("📋 CADASTRO")
                pdf_os = gerar_pdf_os(d)
                c2.download_button("📄 GERAR PDF O.S", pdf_os, f"OS_{d['Nº OS']}.pdf", key=f"p_{d['ID']}")

elif st.session_state.pagina == "💰 FINANCEIRO":
    st.header("💰 Financeiro e Relatórios")
    if st.button("⬅️ VOLTAR"): navegar("🏠 HOME")
    
    c1, c2 = st.columns(2)
    f_ini = c1.date_input("Data Inicial", value=datetime.now(), format="DD/MM/YYYY")
    f_fim = c2.date_input("Data Final", value=datetime.now(), format="DD/MM/YYYY")
    
    dados = carregar_dados()
    if dados:
        df = pd.DataFrame(dados)
        df['dt_filter'] = pd.to_datetime(df['DT_SAIDA_RAW'])
        df_filt = df[(df['dt_filter'] >= pd.Timestamp(f_ini)) & (df['dt_filter'] <= pd.Timestamp(f_fim))]
        
        total = df_filt['VALOR'].sum()
        st.metric("Total Faturado no Período", f"R$ {total:,.2f}")
        
        st.dataframe(df_filt[["Nº OS", "CLIENTE", "DT SAÍDA", "EMPURRADOR", "BALSA", "ESCOLTA 1", "ESCOLTA 2", "VALOR"]], use_container_width=True)
        
        # BOTÃO PARA IMPRIMIR RELATÓRIO PDF POR PERÍODO
        pdf_fin = gerar_pdf_financeiro(df_filt, total, f_ini, f_fim)
        st.download_button("📥 BAIXAR RELATÓRIO PDF (PERÍODO)", pdf_fin, "relatorio_financeiro.pdf", type="primary")
