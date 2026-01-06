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

# --- ESTILO CSS (BOTÃO VERDE E DESIGN) ---
st.markdown("""
    <style>
    div.stButton > button:first-child[kind="primary"] { background-color: #28a745; color: white; border: none; }
    .stButton>button { width: 100%; border-radius: 8px; font-weight: bold; height: 3.5em; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNÇÃO GERAR PDF (MODELO TRANSDOURADA) ---
def gerar_pdf_transdourada(d):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 10)
    pdf.cell(0, 5, "ZION TECNOLOGIA | TRANSDOURADA", ln=True)
    pdf.ln(10)
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Solicitação de Escolta", ln=True, align="C")
    pdf.cell(0, 7, f"O.S: {d.get('Nº OS', '---')}", ln=True, align="C")
    pdf.ln(5)
    pdf.cell(0, 10, f"SOLICITANTE ( {d.get('CLIENTE', '---').upper()} )", border=1, ln=True, align="C")
    pdf.ln(5)
    pdf.set_font("Arial", "", 10)
    pdf.multi_cell(0, 6, f"DESCRIÇÃO: {d.get('DESCRIÇÃO', '---')}")
    pdf.set_y(-35)
    pdf.set_font("Arial", "B", 7)
    pdf.cell(0, 5, "TRANSDOURADA N
