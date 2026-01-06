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
    .stButton>button { width: 100%; border-radius: 8px; font-weight: bold; height: 3.5em; background-color: #0047AB; color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNÇÃO GERAR PDF (ESTILO TRANSDOURADA) ---
def gerar_pdf_os(d):
    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 10)
        pdf.cell(0, 5, "ZION TECNOLOGIA | TRANSDOURADA", ln=True)
        pdf.ln(10)
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, "Solicitação de Escolta", ln=True, align="C")
        pdf.set_font("Arial", "B", 11)
        pdf.cell(0, 7, f"ORDEM DE SERVIÇO O.S: {d.get('Nº OS', '---')}", ln=True, align="C")
        pdf.ln(5)
        pdf.cell(0, 10, f"SOLICITANTE ( {d.get('CLIENTE', '---')} )", border=1, ln=True, align="C")
        pdf.ln(5)
        pdf.set_font("Arial", "", 10)
        pdf.multi_cell(0, 6, f"DETALHAMENTO: {d.get('DESCRIÇÃO', '---')}")
        return pdf.output(dest="S").encode("latin-1")
    except:
        return b""

# --- NAVEGAÇÃO ---
if "pagina" not in st.session_state:
    st.session_state.pagina = "🏠 HOME"

def navegar(p):
    st.session_state.pagina = p
    st.rerun()

# --- TELA HOME ---
if st.session_state.pagina == "🏠 HOME":
    if os.path.exists("LOGO.PNG"):
        st.image("LOGO.PNG", width=250)
    st.title("🛡️ Painel de Controle Zion")
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📋 NOVO LANÇAMENTO"): navegar("📋 CADASTRO")
    with col2:
        if st.button("📊 VER AGENDAMENTOS"): navegar("📊 GRADE")
    with col3:
        if st.button("💰 FINANCEIRO"): navegar("💰 FINANCEIRO")

# --- TELA DE CADASTRO ---
elif st.session_state.pagina == "📋 CADASTRO":
    if st.button("⬅️ VOLTAR"): navegar("🏠 HOME")
    st.header("📝 Nova Missão")
    with st.form("form_missao"):
        c1, c2, c3 = st.columns(3)
        os_n = c1.text_input("Nº O.S")
        dt_saida = c2.date_input("DT SAÍDA") # Calendário Restaurado
        ini_m = c3.date_input("INÍCIO DA MISSÃO")
        
        cliente = c1.text_input("CLIENTE")
        empurrador = c2.text_input("EMPURRADOR")
        status = c3.selectbox("STATUS", ["Em Andamento", "Encerrado"])
        
        desc = st.text_area("DESCRIÇÃO / OBSERVAÇÕES")
        
        if st.form_submit_button("✅ SALVAR OPERAÇÃO"):
            payload = {
                "parent": {"database_id": DATABASE},
                "properties": {
                    "Nº OS": {"title": [{"text": {"content": os_n}}]},
                    "CLIENTE": {"rich_text": [{"text": {"content": cliente}}]},
                    "DT SAÍDA": {"date": {"start": str(dt_saida)}},
                    "INÍCIO DA MISSÃO": {"date": {"start": str(ini_m)}},
                    "STATUS": {"select": {"name": status}},
                    "EMPURRADOR": {"rich_text": [{"text": {"content": empurrador}}]},
                    "DESCRIÇÃO": {"rich_text": [{"text": {"content": desc}}]}
                }
            }
            res = requests.post("https://api.notion.com/v1/pages", headers=headers, json=payload)
            if res.status_code == 200:
                st.success("🎯 Salvo!"); navegar("🏠 HOME")
            else:
                st.error("Erro ao salvar no Notion.")

# --- TELA GRADE ---
elif st.session_state.pagina == "📊 GRADE":
    if st.button("⬅️ VOLTAR"): navegar("🏠 HOME")
    st.subheader("📊 Agendamentos Ativos")
    st.write("Abaixo estão as missões registradas no Notion.")
    # Aqui você pode adicionar sua lógica de carregar_dados() se desejar listar

# --- TELA FINANCEIRO (RESTAURADA) ---
elif st.session_state.pagina == "💰 FINANCEIRO":
    if st.button("⬅️ VOLTAR"): navegar("🏠 HOME")
    st.header("💰 Controle Financeiro")
    
    # Criando uma tabela vazia conforme solicitado
    df_vazio = pd.DataFrame(columns=["DATA", "DESCRIÇÃO", "TIPO", "VALOR (R$)", "STATUS"])
    
    st.subheader("Resumo de Lançamentos")
    st.table(df_vazio) # Aparece pelo menos a estrutura da tabela
    
    st.info("O módulo financeiro está sendo integrado ao seu banco de dados.")
