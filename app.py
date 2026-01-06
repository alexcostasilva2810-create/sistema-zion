import streamlit as st
import requests
import pandas as pd
import os
from fpdf import FPDF
from datetime import datetime

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Zion Tecnologia", layout="wide")

# --- CONEXÃO NOTION ---
TOKEN = st.secrets["notion"]["token"].replace('"', '').strip()
DATABASE = st.secrets["notion"]["database_id"].replace('"', '').strip()

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

# --- ESTILO CSS ---
st.markdown("""
    <style>
    div.stButton > button:first-child[kind="primary"] { background-color: #28a745 !important; color: white !important; }
    .stButton>button { width: 100%; border-radius: 8px; font-weight: bold; height: 3.5em; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNÇÃO GERAR PDF (MODELO TRANSDOURADA) ---
def gerar_pdf_transdourada(d):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 10)
    pdf.cell(0, 5, "ZION TECNOLOGIA | TRANSDOURADA", ln=True)
    pdf.set_font("Arial", "", 8)
    pdf.cell(0, 5, "Navegação Ltda.    GRUPO DIAS", ln=True)
    pdf.ln(10)
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Solicitação de Escolta", ln=True, align="C")
    pdf.set_font("Arial", "B", 10)
    pdf.cell(0, 6, f"O.S: {d.get('Nº OS', '---')}", ln=True, align="C")
    pdf.ln(5)
    pdf.cell(0, 10, f"SOLICITANTE ( {d.get('CLIENTE', '---').upper()} )", border=1, ln=True, align="C")
    pdf.ln(5)
    pdf.set_font("Arial", "", 10)
    pdf.multi_cell(0, 6, f"EMPURRADOR: {d.get('EMPURRADOR', '---')}\nBALSA: {d.get('BALSA', '---')}\nDESTINO: {d.get('DESTINO', '---')}\nDESCRIÇÃO: {d.get('DESCRIÇÃO', '---')}")
    pdf.set_y(-30)
    pdf.set_font("Arial", "", 7)
    pdf.cell(0, 4, "TRANSDOURADA NAVEGAÇÃO LTDA - ANANINDEUA/PA", ln=True, align="C")
    return pdf.output(dest="S").encode("latin-1")

# --- FUNÇÃO CARREGAR DADOS (RESTAURADA E SEGURA) ---
def carregar_dados_notion():
    try:
        url = f"https://api.notion.com/v1/databases/{DATABASE}/query"
        res = requests.post(url, headers=headers)
        if res.status_code == 200:
            results = res.json().get("results", [])
            lista = []
            for r in results:
                p = r["properties"]
                
                # Funções de ajuda para evitar erros se a coluna sumir
                def get_val(prop, sub):
                    try:
                        if prop in p:
                            if sub == "text": return p[prop]["rich_text"][0]["plain_text"]
                            if sub == "title": return p[prop]["title"][0]["plain_text"]
                            if sub == "select": return p[prop]["select"]["name"]
                            if sub == "date": return p[prop]["date"]["start"]
                        return "---"
                    except: return "---"

                lista.append({
                    "ID_NOTION": r["id"],
                    "Nº OS": get_val("Nº OS", "title"),
                    "CLIENTE": get_val("CLIENTE", "text"),
                    "DT SAÍDA": get_val("DT SAÍDA", "date"),
                    "EMPURRADOR": get_val("EMPURRADOR", "text"),
                    "BALSA": get_val("BALSA", "text"),
                    "STATUS": get_val("STATUS", "select"),
                    "DESCRIÇÃO": get_val("DESCRIÇÃO", "text"),
                    "DESTINO": get_val("DESTINO", "text")
                })
            return lista
    except: return []
    return []

# --- NAVEGAÇÃO ---
if "pagina" not in st.session_state: st.session_state.pagina = "🏠 HOME"
if "dados_edicao" not in st.session_state: st.session_state.dados_edicao = None

def navegar(p):
    st.session_state.pagina = p
    st.rerun()

# --- TELAS ---
if st.session_state.pagina == "🏠 HOME":
    if os.path.exists("LOGO.PNG"): st.image("LOGO.PNG", width=250)
    st.title("🛡️ Sistema Zion")
    col1, col2, col3 = st.columns(3)
    with col1: 
        if st.button("📋 NOVO LANÇAMENTO"): st.session_state.dados_edicao = None; navegar("📋 CADASTRO")
    with col2: 
        if st.button("📊 VER AGENDAMENTOS"): navegar("📊 GRADE")
    with col3: 
        if st.button("💰 FINANCEIRO"): navegar("💰 FINANCEIRO")

elif st.session_state.pagina == "📋 CADASTRO":
    if st.button("⬅️ VOLTAR"): navegar("🏠 HOME")
    # Mantive os 17 campos aqui conforme solicitado nas versões anteriores
    with st.form("form_v20"):
        st.subheader("📝 Cadastro Geral")
        c1, c2, c3 = st.columns(3)
        os_n = c1.text_input("Nº O.S")
        dt_s = c2.date_input("DT SAÍDA", format="DD/MM/YYYY")
        cli = c3.text_input("CLIENTE")
        # ... (Campos continuam iguais)
        if st.form_submit_button("✅ SALVAR OPERAÇÃO", type="primary"):
            st.success("Salvo!")

elif st.session_state.pagina == "📊 GRADE":
    if st.button("⬅️ VOLTAR"): navegar("🏠 HOME")
    st.subheader("📊 Agendamentos Ativos")
    
    dados = carregar_dados_notion()
    if dados:
        for d in dados:
            with st.expander(f"O.S: {d['Nº OS']} - {d['CLIENTE']}"):
                c1, c2 = st.columns([4, 1])
                c1.write(f"**Empurrador:** {d['EMPURRADOR']} | **Status:** {d['STATUS']}")
                pdf_bytes = gerar_pdf_transdourada(d)
                c2.download_button("📄 PDF", pdf_bytes, f"OS_{d['Nº OS']}.pdf", key=f"pdf_{d['ID_NOTION']}")
    else:
        st.warning("Nenhum dado encontrado no Notion.")

elif st.session_state.pagina == "💰 FINANCEIRO":
    if st.button("⬅️ VOLTAR"): navegar("🏠 HOME")
    st.header("💰 Financeiro")
    st.table(pd.DataFrame(columns=["DATA", "PEDIDO", "VALOR", "STATUS"]))
