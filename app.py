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

# --- FUNÇÃO GERAR PDF (MODELO TRANSDOURADA) ---
def gerar_pdf_os(d):
    try:
        pdf = FPDF()
        pdf.add_page()
        
        # Cabeçalho
        pdf.set_font("Arial", "B", 10)
        pdf.cell(0, 5, "ZION TECNOLOGIA | TRANSDOURADA", ln=True)
        pdf.ln(10)

        # Títulos
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, "Solicitação de Escolta", ln=True, align="C")
        pdf.set_font("Arial", "B", 11)
        pdf.cell(0, 7, f"ORDEM DE SERVIÇO O.S: {d.get('Nº OS', '---')}", ln=True, align="C")
        pdf.ln(2)

        # Caixa Solicitante
        pdf.cell(0, 10, f"SOLICITANTE ( {d.get('CLIENTE', '---')} )", border=1, ln=True, align="C")
        pdf.ln(5)

        # Dados da Missão
        pdf.set_font("Arial", "", 9)
        pdf.multi_cell(0, 6, f"EMPURRADOR: {d.get('EMPURRADOR', '---')}\nBALSA: {d.get('BALSA', '---')}\nLOCAL: {d.get('LOCAL', '---')}\nDESTINO: {d.get('DESTINO', '---')}", border=1)
        
        pdf.ln(5)
        pdf.set_font("Arial", "B", 11)
        pdf.cell(0, 10, "PVH-SEG Serv. de Vig. Patrimonial Ltda", border=1, ln=True, align="C")
        
        pdf.ln(5)
        pdf.set_font("Arial", "", 10)
        pdf.cell(0, 6, f"INÍCIO DA MISSÃO: {d.get('INÍCIO', '---')}", ln=True)
        pdf.cell(0, 6, f"FIM DA MISSÃO: {d.get('DT SAÍDA', '---')}", ln=True)
        
        pdf.ln(10)
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, "DETALHAMENTO DA MISSÃO.", ln=True, align="C")
        pdf.set_font("Arial", "", 10)
        # CORREÇÃO: multi_cell agora fecha corretamente sem erro de sintaxe
        pdf.multi_cell(0, 6, f"DESCRIÇÃO: {d.get('DESCRIÇÃO', '---')}")

        return pdf.output(dest="S").encode("latin-1")
    except Exception as e:
        return str(e).encode("latin-1")

# --- NAVEGAÇÃO ---
if "pagina" not in st.session_state:
    st.session_state.pagina = "🏠 HOME"

def navegar(p):
    st.session_state.pagina = p
    st.rerun()

# --- TELA HOME ---
if st.session_state.pagina == "🏠 HOME":
    st.title("🛡️ Sistema Zion Tecnologia")
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📝 NOVO LANÇAMENTO"): navegar("📋 CADASTRO")
    with col2:
        if st.button("📊 VER AGENDAMENTOS"): navegar("📊 GRADE")
    with col3:
        if st.button("💰 FINANCEIRO"): navegar("💰
