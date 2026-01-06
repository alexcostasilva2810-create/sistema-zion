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

# --- CSS PARA GRADE PROFISSIONAL ---
st.markdown("""
    <style>
    .grade-zion { width: 100%; border-collapse: collapse; background-color: white; color: black; font-size: 13px; }
    .grade-zion th { border: 2px solid #000000 !important; background-color: #f0f2f6; padding: 10px; text-align: left; font-weight: bold; }
    .grade-zion td { border: 2px solid #000000 !important; padding: 8px; }
    .stButton>button { width: 100%; border-radius: 5px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNÇÃO GERAR PDF (MODELO TRANSDOURADA) ---
def gerar_pdf_modelo_transdourada(d):
    pdf = FPDF()
    pdf.add_page()
    
    # Cabeçalho Simulado (Texto substitui imagem se não houver arquivo)
    pdf.set_font("Arial", "B", 10)
    pdf.cell(0, 5, "ZION TECNOLOGIA | TRANSDOURADA", ln=True)
    pdf.set_font("Arial", "", 8)
    pdf.cell(0, 5, "Navegação Ltda.    GRUPO DIAS", ln=True)
    pdf.ln(10)

    # Títulos Centralizados
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Solicitação de Escolta", ln=True, align="C")
    pdf.set_font("Arial", "B", 11)
    pdf.cell(0, 7, "ORDEM DE SERVIÇO", ln=True, align="C")
    pdf.cell(0, 7, f"O.S: {d['Nº OS']}", ln=True, align="C")
    pdf.cell(0, 7, f"STATUS: {d['STATUS']}", ln=True, align="C")
    pdf.ln(2)

    # Caixa Solicitante
    pdf.cell(0, 10, f"SOLICITANTE ( {d['CLIENTE']} )", border=1, ln=True, align="C")
    pdf.ln(5)

    # Grid de Informações (Simulando colunas da imagem)
    pdf.set_font("Arial", "", 9)
    y_atual = pdf.get_y()
    pdf.text(10, y_atual, f"EMPURRADOR: {d.get('EMPURRADOR', '---')}")
    pdf.text(80, y_atual, f"SAÍDA PREVISTA: {d.get('HORA_EMBARQUE', '---')}")
    pdf.text(150, y_atual, f"STATUS: {d['STATUS']}")
    
    pdf.text(10, y_atual+6, f"ORIGEM: {d.get('LOCAL', '---')}")
    pdf.text(80, y_atual+6, f"DESTINO: {d.get('DESTINO', '---')}")
    pdf.text(150, y_atual+6, f"SERVIÇO: {d['SERVIÇO']}")
    
    pdf.text(10, y_atual+12, f"BALSA: {d.get('BALSA', '---')}")
    pdf.ln(18)

    # Caixa PVH-SEG
    pdf.set_font("Arial", "B", 11)
    pdf.cell(0, 10, "PVH-SEG Serv. de Vig. Patrimonial Ltda", border=1, ln=True, align="C")
    pdf.ln(5)

    # Datas e Escoltas
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

    # Assinatura e Rodapé
    pdf.set_y(-40)
    pdf.cell(0, 0, "", border="T", ln=True)
    pdf.cell(0, 10, "ASSINATURA RESPONSÁVEL", ln=True, align="C")
    pdf.set_font("Arial", "B", 7)
    pdf.cell(0, 5, "TRANSDOURADA NAVEGAÇÃO LTDA - ANANINDEUA/PA", ln=True, align="C")

    return pdf.output(dest="S").encode("latin-1")

# --- BUSCAR DADOS DO NOTION ---
def carregar_dados():
    try:
        url = f"https://api.notion.com/v1/databases/{DATABASE}/query"
        res = requests.post(url, headers=headers)
        if res.status_code == 200:
            results = res.json().get("results", [])
            lista = []
            for r in results:
                p = r["properties"]
                lista.append({
                    "ID": r["id"],
                    "Nº OS": p["Nº OS"]["title"][0]["plain_text"] if p["Nº OS"]["title"] else "---",
                    "CLIENTE": p["CLIENTE"]["rich_text"][0]["plain_text"] if p["CLIENTE"]["rich_text"] else "---",
                    "INÍCIO": p["INÍCIO DA MISSÃO"]["date"]["start"] if p["INÍCIO DA MISSÃO"]["date"] else "---",
                    "DT SAÍDA": p["DT SAÍDA"]["date"]["start"] if p["DT SAÍDA"]["date"] else "---",
                    "SERVIÇO": p["SERVIÇO"]["select"]["name"] if p["SERVIÇO"]["select"] else "---",
                    "STATUS": p["STATUS"]["select"]["name"] if p["STATUS"]["select"] else "---",
                    "EMPURRADOR": p["EMPURRADOR"]["rich_text"][0]["plain_text"] if p["EMPURRADOR"]["rich_text"] else "---",
                    "BALSA": p["BALSA"]["rich_text"][0]["plain_text"] if p["BALSA"]["rich_text"] else "---",
                    "DESCRIÇÃO": p["DESCRIÇÃO"]["rich_text"][0]["plain_text"] if p["DESCRIÇÃO"]["rich_text"] else "---",
                    "ESCOLTA 1": p["ESCOLTA 1"]["rich_text"][0]["plain_text"] if p["ESCOLTA 1"]["rich_text"] else "---",
                    "ESCOLTA 2": p["ESCOLTA 2"]["rich_text"][0]["plain_text"] if p["ESCOLTA 2"]["rich_text"] else "---"
                })
            return lista
    except: return []
    return []

# --- NAVEGAÇÃO ---
if "pagina" not in st.session_state: st.session_state.pagina = "🏠 HOME"

# --- TELA HOME ---
if st.session_state.pagina == "🏠 HOME":
    col_logo, col_vazia = st.columns([1, 2])
    with col_logo:
        if os.path.exists("LOGO.PNG"): st.image("LOGO.PNG", width=300)
    
    st.subheader("📋 Grade de Agendamentos (Notion)")
    
    dados = carregar_dados()
    if dados:
        # Cabeçalho da Grade
        c = st.columns([1, 2, 1.2, 1.2, 1.2, 1.2, 0.8])
        cols_nomes = ["O.S", "CLIENTE", "INÍCIO", "DT SAÍDA", "SERVIÇO", "STATUS", "AÇÕES"]
        for i, nome in enumerate(cols_nomes): c[i].write(f"**{nome}**")
        
        for item in dados:
            c = st.columns([1, 2, 1.2, 1.2, 1.2, 1.2, 0.8])
            c[0].write(item["Nº OS"])
            c[1].write(item["CLIENTE"])
