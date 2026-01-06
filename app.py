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
    .stDownloadButton>button { width: 100%; background-color: #28a745; color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNÇÃO PARA PUXAR DADOS DO NOTION ---
def carregar_dados_notion():
    try:
        url = f"https://api.notion.com/v1/databases/{DATABASE}/query"
        res = requests.post(url, headers=headers)
        if res.status_code == 200:
            results = res.json().get("results", [])
            lista = []
            for r in results:
                p = r["properties"]
                lista.append({
                    "Nº OS": p["Nº OS"]["title"][0]["plain_text"] if p["Nº OS"]["title"] else "---",
                    "CLIENTE": p["CLIENTE"]["rich_text"][0]["plain_text"] if p["CLIENTE"]["rich_text"] else "---",
                    "DT SAÍDA": p["DT SAÍDA"]["date"]["start"] if p["DT SAÍDA"]["date"] else "---",
                    "EMPURRADOR": p["EMPURRADOR"]["rich_text"][0]["plain_text"] if p["EMPURRADOR"]["rich_text"] else "---",
                    "STATUS": p["STATUS"]["select"]["name"] if p["STATUS"]["select"] else "---",
                    "SERVIÇO": p["SERVIÇO"]["select"]["name"] if p["SERVIÇO"]["select"] else "---",
                    "DESCRIÇÃO": p["DESCRIÇÃO"]["rich_text"][0]["plain_text"] if p["DESCRIÇÃO"]["rich_text"] else ""
                })
            return lista
    except: return []
    return []

# --- NAVEGAÇÃO ---
if "pagina" not in st.session_state: st.session_state.pagina = "🏠 HOME"
def navegar(p): st.session_state.pagina = p; st.rerun()

# --- TELA HOME (LOGO RESTAURADA) ---
if st.session_state.pagina == "🏠 HOME":
    if os.path.exists("LOGO.PNG"):
        st.image("LOGO.PNG", width=300)
    else:
        st.title("🛡️ Zion Tecnologia")
        
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📋 NOVO LANÇAMENTO"): navegar("📋 CADASTRO")
    with col2:
        if st.button("📊 VER AGENDAMENTOS"): navegar("📊 GRADE")
    with col3:
        if st.button("💰 FINANCEIRO"): navegar("💰 FINANCEIRO")

# --- TELA DE CADASTRO (17 CAMPOS COMPLETOS) ---
elif st.session_state.pagina == "📋 CADASTRO":
    if st.button("⬅️ VOLTAR"): navegar("🏠 HOME")
    st.header("📝 Cadastro Geral de Missão")
    
    with st.form("form_completo"):
        c1, c2, c3 = st.columns(3)
        os_n = c1.text_input("Nº O.S")
        dt_saida = c2.date_input("DT SAÍDA")
        cliente = c3.text_input("CLIENTE")
        
        c4, c5, c6 = st.columns(3)
        ini_m = c4.date_input("INÍCIO DA MISSÃO")
        fim_m = c5.date_input("FIM DA MISSÃO")
        balsa = c6.text_input("BALSA")
        
        c7, c8, c9 = st.columns(3)
        h_emb = c7.text_input("HORA DE EMBARQUE")
        esc1 = c8.text_input("ESCOLTA 1")
        destino = c9.text_input("DESTINO")
        
        c10, c11, c12 = st.columns(3)
        local = c10.text_input("LOCAL")
        esc2 = c11.text_input("ESCOLTA 2")
        pedido = c12.text_input("PEDIDO")
        
        c13, c14, c15 = st.columns(3)
        empurrador = c13.text_input("EMPURRADOR")
        servico = c14.selectbox("SERVIÇO", ["Escolta", "Vigilância"])
        ass_resp = c15.text_input("ASSINATURA RESPONSÁVEL")
        
        desc = st.text_area("DESCRIÇÃO / OBSERVAÇÕES")
        status = st.selectbox("STATUS", ["Em Andamento", "Encerrado"])
        
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
            else: st.error("Erro ao salvar.")

# --- TELA GRADE (PUXANDO DO NOTION) ---
elif st.session_state.pagina == "📊 GRADE":
    if st.button("⬅️ VOLTAR"): navegar("🏠 HOME")
    st.subheader("📋 Grade de Agendamentos (Notion Real)")
    
    dados = carregar_dados_notion()
    if dados:
        df = pd.DataFrame(dados)
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.warning("Nenhum dado encontrado no Notion ou erro de conexão.")

# --- TELA FINANCEIRO ---
elif st.session_state.pagina == "💰 FINANCEIRO":
    if st.button("⬅️ VOLTAR"): navegar("🏠 HOME")
    st.header("💰 Controle Financeiro")
    df_financeiro = pd.DataFrame(columns=["DATA", "PEDIDO", "CLIENTE", "VALOR", "STATUS"])
    st.table(df_financeiro)
