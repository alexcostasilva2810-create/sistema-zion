import streamlit as st
import requests
import pandas as pd
import os
import base64
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

# --- CSS PARA GRADE E BOTÕES ---
st.markdown("""
    <style>
    .grade-zion { width: 100%; border-collapse: collapse; background-color: white; color: black; font-size: 13px; }
    .grade-zion th { border: 2px solid #000000 !important; background-color: #f0f2f6; padding: 10px; text-align: left; }
    .grade-zion td { border: 2px solid #000000 !important; padding: 8px; }
    .stButton>button { width: 100%; border-radius: 8px; font-weight: bold; height: 3em; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNÇÃO GERAR PDF (MODELO TRANSDOURADA REPLICADO) ---
def gerar_pdf_os(d):
    pdf = FPDF()
    pdf.add_page()
    
    # Cabeçalho Logos (Texto simulado)
    pdf.set_font("Arial", "B", 10)
    pdf.cell(0, 5, "ZION TECNOLOGIA | TRANSDOURADA", ln=True)
    pdf.set_font("Arial", "", 8)
    pdf.cell(0, 5, "Navegação Ltda.    GRUPO DIAS", ln=True)
    pdf.ln(10)

    # Títulos
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Solicitação de Escolta", ln=True, align="C")
    pdf.set_font("Arial", "B", 11)
    pdf.cell(0, 7, "ORDEM DE SERVIÇO", ln=True, align="C")
    pdf.cell(0, 7, f"O.S: {d['Nº OS']}", ln=True, align="C")
    pdf.set_font("Arial", "", 10)
    pdf.cell(0, 7, f"STATUS: {d['STATUS'].upper()}", ln=True, align="C")
    pdf.ln(2)

    # Caixa Solicitante
    pdf.set_font("Arial", "B", 11)
    pdf.cell(0, 10, f"SOLICITANTE ( {d['CLIENTE'].upper()} )", border=1, ln=True, align="C")
    pdf.ln(5)

    # Grid Técnico (Simulando colunas do anexo)
    pdf.set_font("Arial", "", 9)
    y = pdf.get_y()
    pdf.text(10, y, f"EMPURRADOR: {d.get('EMPURRADOR', '---')}")
    pdf.text(80, y, f"SAÍDA PREVISTA: {d.get('HORA_EMBARQUE', '---')}")
    pdf.text(150, y, f"STATUS: {d['STATUS']}")
    
    pdf.text(10, y+6, f"ORIGEM: {d.get('LOCAL', '---')}")
    pdf.text(80, y+6, f"DESTINO: {d.get('DESTINO', '---')}")
    pdf.text(150, y+6, f"SERVIÇO: {d['SERVIÇO']}")
    
    pdf.text(10, y+12, f"BALSA: {d.get('BALSA', '---')}")
    pdf.ln(20)

    # Segunda Caixa
    pdf.set_font("Arial", "B", 11)
    pdf.cell(0, 10, "PVH-SEG Serv. de Vig. Patrimonial Ltda", border=1, ln=True, align="C")
    pdf.ln(5)

    # Dados Missão
    pdf.set_font("Arial", "", 10)
    pdf.cell(0, 6, f"INÍCIO DA MISSÃO: {d['INÍCIO']}", ln=True)
    pdf.cell(0, 6, f"ESCOLTA 1: {d.get('ESCOLTA 1', '---')}", ln=True)
    pdf.cell(0, 6, f"ESCOLTA 2: {d.get('ESCOLTA 2', '---')}", ln=True)
    pdf.cell(0, 6, f"FIM DA MISSÃO: {d['DT SAÍDA']}", ln=True)
    
    pdf.ln(5)
    pdf.cell(190, 0, "", border="T", ln=True)
    pdf.ln(5)

    # Detalhamento
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "DETALHAMENTO DA MISSÃO.", ln=True, align="C")
    pdf.set_font("Arial", "", 10)
    pdf.multi_cell(0, 6, f"DESCRIÇÃO: {d.get('DESCRIÇÃO', '---')}")

    # Rodapé e Assinatura
    pdf.set_y(-45)
    pdf.cell(190, 0, "", border="T", ln=True)
    pdf.cell(0, 10, "ASSINATURA RESPONSÁVEL", ln=True, align="C")
    pdf.set_font("Arial", "B", 7)
    pdf.cell(0, 5, "TRANSDOURADA NAVEGAÇÃO LTDA - ANANINDEUA/PA", ln=True, align="C")

    return pdf.output(dest="S").encode("latin-1")

# --- FUNÇÃO BUSCAR NOTION ---
def carregar_dados():
    try:
        url = f"https://api.notion.com/v1/databases/{DATABASE}/query"
        res =
