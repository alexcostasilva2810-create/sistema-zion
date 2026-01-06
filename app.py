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

# --- CSS PARA DESIGN ---
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 8px; font-weight: bold; height: 3.5em; background-color: #f0f2f6; }
    .grade-zion { width: 100%; border-collapse: collapse; }
    .grade-zion th { border: 2px solid #000; background-color: #eee; padding: 8px; }
    .grade-zion td { border: 2px solid #000; padding: 8px; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNÇÃO GERAR PDF (EXATAMENTE COMO O MODELO ENVIADO) ---
def gerar_pdf_os(d):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Solicitação de Escolta", ln=True, align="C")
    pdf.set_font("Arial", "B", 10)
    pdf.cell(0, 7, f"ORDEM DE SERVIÇO O.S: {d['Nº OS']}", ln=True, align="C")
    pdf.ln(5)
    
    # Caixa Solicitante
    pdf.cell(0, 10, f"SOLICITANTE ( {d['CLIENTE']} )", border=1, ln=True, align="C")
    pdf.ln(5)
    
    # Informações Técnicas
    pdf.set_font("Arial", "", 9)
    info = f"EMPURRADOR: {d.get('EMPURRADOR', '---')}    ORIGEM: {d.get('LOCAL', '---')}    DESTINO: {d.get('DESTINO', '---')}"
    pdf.multi_cell(0, 8, info, border=1)
    
    pdf.ln(5)
    pdf.set_font("Arial", "B", 10)
    pdf.cell(0, 10, "PVH-SEG Serv. de Vig. Patrimonial Ltda", border=1, ln=True, align="C")
    
    pdf.set_font("Arial", "", 9)
    pdf.ln(5)
    pdf.cell(0, 7, f"INÍCIO DA MISSÃO: {d['INÍCIO']}", ln=True)
    pdf.cell(0, 7, f"ESCOLTA 1: {d.get('ESCOLTA 1', '---')}", ln=True)
    pdf.cell(0, 7, f"ESCOLTA 2: {d.get('ESCOLTA 2', '---')}", ln=True)
    pdf.cell(0, 7, f"FIM DA MISSÃO: {d['DT SAÍDA']}", ln=True)
    
    pdf.ln(10)
    pdf.set_font("Arial", "B", 11)
    pdf.cell(0, 7, "DETALHAMENTO DA MISSÃO", ln=True)
    pdf.set_font("Arial", "", 10)
    pdf.multi_cell(0
