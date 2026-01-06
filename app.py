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

# --- TELA DE CADASTRO (TODAS AS COLUNAS RESTAURADAS) ---
elif st.session_state.pagina == "📋 CADASTRO":
    if st.button("⬅️ VOLTAR"): navegar("🏠 HOME")
    st.header("📝 Cadastro Geral de Missão")
    
    with st.form("form_completo"):
        # Linha 1
        c1, c2, c3 = st.columns(3)
        os_n = c1.text_input("Nº O.S")
        dt_saida = c2.date_input("DT SAÍDA") # CALENDÁRIO FIXADO
        cliente = c3.text_input("CLIENTE")
        
        # Linha 2
        c4, c5, c6 = st.columns(3)
        ini_m = c4.date_input("INÍCIO DA MISSÃO")
        fim_m = c5.date_input("FIM DA MISSÃO")
        balsa = c6.text_input("BALSA")
        
        # Linha 3
        c7, c8, c9 = st.columns(3)
        h_emb = c7.text_input("HORA DE EMBARQUE")
        esc1 = c8.text_input("ESCOLTA 1")
        destino = c9.text_input("DESTINO")
        
        # Linha 4
        c10, c11, c12 = st.columns(3)
        local = c10.text_input("LOCAL")
        esc2 = c11.text_input("ESCOLTA 2")
        pedido = c12.text_input("PEDIDO")
        
        # Linha 5
        c13, c14, c15 = st.columns(3)
        empurrador = c13.text_input("EMPURRADOR")
        servico = c14.selectbox("SERVIÇO", ["Escolta", "Vigilância"])
        ass_resp = c15.text_input("ASSINATURA RESPONSÁVEL")
        
        # Linha 6
        c16, c17 = st.columns([2, 1])
        desc = c16.text_area("DESCRIÇÃO / OBSERVAÇÕES")
        status = c17.selectbox("STATUS", ["Em Andamento", "Encerrado", "Cancelado"])
        
        if st.form_submit_button("✅ SALVAR OPERAÇÃO"):
            payload = {
                "parent": {"database_id": DATABASE},
                "properties": {
                    "Nº OS": {"title": [{"text": {"content": os_n}}]},
                    "CLIENTE": {"rich_text": [{"text": {"content": cliente}}]},
                    "DT SAÍDA": {"date": {"start": str(dt_saida)}},
                    "INÍCIO DA MISSÃO": {"date": {"start": str(ini_m)}},
                    "FIM DA MISSÃO": {"date": {"start": str(fim_m)}},
                    "STATUS": {"select": {"name": status}},
                    "SERVIÇO": {"select": {"name": servico}},
                    "EMPURRADOR": {"rich_text": [{"text": {"content": empurrador}}]},
                    "BALSA": {"rich_text": [{"text": {"content": balsa}}]},
                    "ESCOLTA 1": {"rich_text": [{"text": {"content": esc1}}]},
                    "ESCOLTA 2": {"rich_text": [{"text": {"content": esc2}}]},
                    "LOCAL": {"rich_text": [{"text": {"content": local}}]},
                    "DESTINO": {"rich_text": [{"text": {"content": destino}}]},
                    "DESCRIÇÃO": {"rich_text": [{"text": {"content": desc}}]}
                    # Adicione aqui outros campos conforme configurados no seu Notion
                }
            }
            res = requests.post("https://api.notion.com/v1/pages", headers=headers, json=payload)
            if res.status_code == 200:
                st.success("🎯 Missão salva com sucesso!")
                navegar("🏠 HOME")
            else:
                st.error(f"Erro ao salvar: {res.text}")

# --- TELA GRADE ---
elif st.session_state.pagina == "📊 GRADE":
    if st.button("⬅️ VOLTAR"): navegar("🏠 HOME")
    st.subheader("📊 Grade de Agendamentos")
    st.info("Lista de missões ativas carregadas do Notion.")

# --- TELA FINANCEIRO ---
elif st.session_state.pagina == "💰 FINANCEIRO":
    if st.button("⬅️ VOLTAR"): navegar("🏠 HOME")
    st.header("💰 Controle Financeiro")
    df_financeiro = pd.DataFrame(columns=["DATA", "PEDIDO", "CLIENTE", "VALOR (R$)", "STATUS"])
    st.table(df_financeiro)
    st.info("Tabela financeira pronta para receber dados.")
