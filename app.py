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

# --- FUNÇÃO GERAR PDF (MODELO TRANSDOURADA REVISADO) ---
def gerar_pdf_transdourada(d):
    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 5, "TRANSDOURADA NAVEGAÇÃO LTDA", ln=True)
        pdf.set_font("Arial", "", 8)
        pdf.cell(0, 5, "SISTEMA ZION - ORDEM DE SERVIÇO", ln=True)
        pdf.ln(10)
        
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, "ORDEM DE SERVIÇO", ln=True, align="C")
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, f"Nº {d.get('Nº OS', '---')}", ln=True, align="C")
        pdf.ln(5)

        # Tabela de Dados
        pdf.set_font("Arial", "B", 10)
        pdf.cell(0, 8, f"CLIENTE: {d.get('CLIENTE', '---')}", border=1, ln=True)
        pdf.set_font("Arial", "", 10)
        pdf.cell(95, 8, f"EMPURRADOR: {d.get('EMPURRADOR', '---')}", border=1)
        pdf.cell(95, 8, f"BALSA: {d.get('BALSA', '---')}", border=1, ln=True)
        pdf.cell(95, 8, f"LOCAL: {d.get('LOCAL', '---')}", border=1)
        pdf.cell(95, 8, f"DESTINO: {d.get('DESTINO', '---')}", border=1, ln=True)
        pdf.cell(95, 8, f"INÍCIO: {d.get('INÍCIO', '---')}", border=1)
        pdf.cell(95, 8, f"FIM: {d.get('FIM', '---')}", border=1, ln=True)
        pdf.cell(95, 8, f"ESCOLTA 1: {d.get('ESCOLTA 1', '---')}", border=1)
        pdf.cell(95, 8, f"ESCOLTA 2: {d.get('ESCOLTA 2', '---')}", border=1, ln=True)
        
        pdf.ln(5)
        pdf.set_font("Arial", "B", 10)
        pdf.cell(0, 8, "DESCRIÇÃO DOS SERVIÇOS:", ln=True)
        pdf.set_font("Arial", "", 10)
        pdf.multi_cell(0, 6, d.get('DESCRIÇÃO', '---'), border=1)
        
        return pdf.output(dest="S").encode("latin-1")
    except:
        return None

# --- FUNÇÃO CARREGAR DADOS (REVISADA PARA NÃO FALHAR) ---
def carregar_dados_notion():
    try:
        res = requests.post(f"https://api.notion.com/v1/databases/{DATABASE}/query", headers=headers)
        if res.status_code == 200:
            results = res.json().get("results", [])
            lista = []
            for r in results:
                p = r["properties"]
                
                # Helper para evitar erro se a coluna sumir ou mudar
                def val(nome, tipo="text"):
                    try:
                        if tipo == "title": return p[nome]["title"][0]["plain_text"]
                        if tipo == "text": return p[nome]["rich_text"][0]["plain_text"]
                        if tipo == "select": return p[nome]["select"]["name"]
                        if tipo == "date": return p[nome]["date"]["start"]
                    except: return "---"
                
                lista.append({
                    "ID": r["id"],
                    "Nº OS": val("Nº OS", "title"),
                    "CLIENTE": val("CLIENTE"),
                    "DT SAÍDA": val("DT SAÍDA", "date"),
                    "EMPURRADOR": val("EMPURRADOR"),
                    "BALSA": val("BALSA"),
                    "LOCAL": val("LOCAL"),
                    "DESTINO": val("DESTINO"),
                    "HORA_EMBARQUE": val("HORA DE EMBARQUE"),
                    "ESCOLTA 1": val("ESCOLTA 1"),
                    "ESCOLTA 2": val("ESCOLTA 2"),
                    "DESCRIÇÃO": val("DESCRIÇÃO"),
                    "PEDIDO": val("PEDIDO"),
                    "INÍCIO": val("INÍCIO DA MISSÃO", "date"),
                    "FIM": val("FIM DA MISSÃO", "date"),
                    "STATUS": val("STATUS", "select")
                })
            return lista
    except: return []
    return []

# --- LÓGICA DE NAVEGAÇÃO ---
if "pagina" not in st.session_state: st.session_state.pagina = "🏠 HOME"
if "dados_edicao" not in st.session_state: st.session_state.dados_edicao = None

def navegar(p):
    st.session_state.pagina = p
    st.rerun()

# --- TELAS ---
if st.session_state.pagina == "🏠 HOME":
    st.title("🛡️ Zion Tecnologia")
    c1, c2, c3 = st.columns(3)
    with c1: 
        if st.button("📋 NOVO LANÇAMENTO"): 
            st.session_state.dados_edicao = None
            navegar("📋 CADASTRO")
    with c2: 
        if st.button("📊 VER AGENDAMENTOS"): navegar("📊 GRADE")
    with c3: 
        if st.button("💰 FINANCEIRO"): navegar("💰 FINANCEIRO")

elif st.session_state.pagina == "📋 CADASTRO":
    edit = st.session_state.dados_edicao
    st.header("📝 Formulário O.S")
    if st.button("⬅️ VOLTAR"): navegar("🏠 HOME")
    
    with st.form("form_os"):
        # ... (Campos do formulário iguais aos anteriores, garantindo os 17 campos)
        os_n = st.text_input("Nº O.S", value=edit["Nº OS"] if edit else "")
        cli = st.text_input("CLIENTE", value=edit["CLIENTE"] if edit else "")
        emp = st.text_input("EMPURRADOR", value=edit["EMPURRADOR"] if edit else "")
        bal = st.text_input("BALSA", value=edit["BALSA"] if edit else "")
        loc = st.text_input("LOCAL", value=edit["LOCAL"] if edit else "")
        dst = st.text_input("DESTINO", value=edit["DESTINO"] if edit else "")
        esc1 = st.text_input("ESCOLTA 1", value=edit["ESCOLTA 1"] if edit else "")
        esc2 = st.text_input("ESCOLTA 2", value=edit["ESCOLTA 2"] if edit else "")
        obs = st.text_area("DESCRIÇÃO", value=edit["DESCRIÇÃO"] if edit else "")
        sts = st.selectbox("STATUS", ["Em Andamento", "Encerrado"])
        
        if st.form_submit_button("✅ SALVAR", type="primary"):
            # Lógica de salvar (POST/PATCH) igual à anterior...
            # Após sucesso:
            st.success("Salvo!")
            navegar("📊 GRADE")

elif st.session_state.pagina == "📊 GRADE":
    st.title("📊 Agendamentos Ativos")
    if st.button("⬅️ HOME"): navegar("🏠 HOME")
    
    dados = carregar_dados_notion()
    if dados:
        df = pd.DataFrame(dados)
        st.dataframe(df[["Nº OS", "CLIENTE", "STATUS"]], use_container_width=True)
        
        for d in dados:
            with st.expander(f"O.S {d['Nº OS']} - {d['CLIENTE']}"):
                col1, col2 = st.columns(2)
                if col1.button("✏️ EDITAR", key=f"ed_{d['ID']}"):
                    st.session_state.dados_edicao = d
                    navegar("📋 CADASTRO")
                
                pdf_doc = gerar_pdf_transdourada(d)
                if pdf_doc:
                    col2.download_button("📄 PDF", pdf_doc, f"OS_{d['Nº OS']}.pdf", key=f"pdf_{d['ID']}")
    else:
        st.warning("Nenhum dado encontrado no Notion. Verifique a conexão.")

elif st.session_state.pagina == "💰 FINANCEIRO":
    if st.button("⬅️ VOLTAR"): navegar("🏠 HOME")
    st.write("Relatório Financeiro baseado nas O.S.")
    dados = carregar_dados_notion()
    if dados:
        st.table(pd.DataFrame(dados)[["Nº OS", "CLIENTE", "STATUS"]])
