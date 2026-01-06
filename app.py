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

# --- FUNÇÃO GERAR PDF (PADRÃO TRANSDOURADA) ---
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
        pdf.ln(5)

        # Caixa Solicitante
        pdf.cell(0, 10, f"SOLICITANTE ( {d.get('CLIENTE', '---')} )", border=1, ln=True, align="C")
        pdf.ln(5)

        # Dados
        pdf.set_font("Arial", "", 9)
        info = f"EMPURRADOR: {d.get('EMPURRADOR', '---')} | BALSA: {d.get('BALSA', '---')}"
        pdf.multi_cell(0, 6, info, border=1)
        
        pdf.ln(10)
        pdf.set_font("Arial", "B", 11)
        pdf.cell(0, 7, "DETALHAMENTO DA MISSÃO", ln=True)
        pdf.set_font("Arial", "", 10)
        # CORREÇÃO: fechamento do parêntese garantido abaixo
        pdf.multi_cell(0, 6, d.get('DESCRIÇÃO', 'Sem observações.'))
        
        return pdf.output(dest="S").encode("latin-1")
    except Exception as e:
        return str(e).encode("latin-1")

# --- NAVEGAÇÃO ---
if "pagina" not in st.session_state:
    st.session_state.pagina = "🏠 HOME"

def navegar(p):
    st.session_state.pagina = p
    st.rerun()

# --- TELA HOME (RESTAURAÇÃO DOS ÍCONES) ---
if st.session_state.pagina == "🏠 HOME":
    st.title("🛡️ Sistema Zion Tecnologia")
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📋 NOVO LANÇAMENTO"): navegar("📋 CADASTRO")
    with col2:
        if st.button("📊 VER AGENDAMENTOS"): navegar("📊 GRADE")
    with col3:
        if st.button("💰 FINANCEIRO"): navegar("💰 FINANCEIRO")

# --- TELA DE CADASTRO (CORREÇÃO DT SAÍDA E NOTION) ---
elif st.session_state.pagina == "📋 CADASTRO":
    if st.button("⬅️ VOLTAR"): navegar("🏠 HOME")
    st.header("📋 Cadastro de Missão")
    
    with st.form("form_missao"):
        c1, c2, c3 = st.columns(3)
        os_n = c1.text_input("Nº O.S")
        # FIXADO: Agora abre o calendário corretamente
        dt_saida = c2.date_input("DT SAÍDA", value=datetime.today())
        ini_m = c3.date_input("INÍCIO DA MISSÃO", value=datetime.today())
        
        cliente = c1.text_input("CLIENTE")
        empurrador = c2.text_input("EMPURRADOR")
        balsa = c3.text_input("BALSA")
        
        status = c1.selectbox("STATUS", ["Em Andamento", "Encerrado"])
        servico = c2.selectbox("SERVIÇO", ["Escolta", "Vigilância"])
        desc = st.text_area("DESCRIÇÃO / OBSERVAÇÕES")
        
        if st.form_submit_button("✅ SALVAR OPERAÇÃO"):
            # Payload ajustado: Removi campos que não existem no seu Notion (como VALOR)
            payload = {
                "parent": {"database_id": DATABASE},
                "properties": {
                    "Nº OS": {"title": [{"text": {"content": os_n}}]},
                    "CLIENTE": {"rich_text": [{"text": {"content": cliente}}]},
                    "DT SAÍDA": {"date": {"start": str(dt_saida)}},
                    "INÍCIO DA MISSÃO": {"date": {"start": str(ini_m)}},
                    "STATUS": {"select": {"name": status}},
                    "SERVIÇO": {"select": {"name": servico}},
                    "EMPURRADOR": {"rich_text": [{"text": {"content": empurrador}}]},
                    "BALSA": {"rich_text": [{"text": {"content": balsa}}]},
                    "DESCRIÇÃO": {"rich_text": [{"text": {"content": desc}}]}
                }
            }
            res = requests.post("https://api.notion.com/v1/pages", headers=headers, json=payload)
            if res.status_code == 200:
                st.success("🎯 Salvo com sucesso!"); navegar("🏠 HOME")
            else:
                st.error(f"Erro no Notion: {res.text}")

# --- TELA GRADE ---
elif st.session_state.pagina == "📊 GRADE":
    if st.button("⬅️ VOLTAR"): navegar("🏠 HOME")
    st.info("Puxando agendamentos do Notion...")
