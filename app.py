import streamlit as st
import requests
import pandas as pd
import os
from fpdf import FPDF
from datetime import datetime

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Zion Tecnologia - Gestão O.S", layout="wide")

# --- CONEXÃO NOTION (IMPORTANTE: Verifique se os nomes batem com o seu Notion) ---
TOKEN = st.secrets["notion"]["token"].replace('"', '').strip()
DATABASE = st.secrets["notion"]["database_id"].replace('"', '').strip()

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

# --- FUNÇÃO PARA SALVAR NO NOTION (A PEÇA QUE FALTAVA) ---
def salvar_no_notion(dados):
    url = "https://api.notion.com/v1/pages"
    payload = {
        "parent": {"database_id": DATABASE},
        "properties": {
            "Nº OS": {"title": [{"text": {"content": dados['os_n']}}]},
            "CLIENTE": {"rich_text": [{"text": {"content": dados['cli']}}]},
            "DT SAÍDA": {"date": {"start": dados['dt_s'].strftime('%Y-%m-%d')}},
            "EMPURRADOR": {"rich_text": [{"text": {"content": dados['emp']}}]},
            "BALSA": {"rich_text": [{"text": {"content": dados['bal']}}]},
            "PEDIDO": {"rich_text": [{"text": {"content": dados['ped']}}]},
            "HORA DE EMBARQUE": {"rich_text": [{"text": {"content": dados['h_e']}}]},
            "ESCOLTA 1": {"rich_text": [{"text": {"content": dados['esc1']}}]},
            "ESCOLTA 2": {"rich_text": [{"text": {"content": dados['esc2']}}]},
            "LOCAL": {"rich_text": [{"text": {"content": dados['loc']}}]},
            "DESTINO": {"rich_text": [{"text": {"content": dados['dst']}}]},
            "ASSINATURA RESPONSÁVEL": {"rich_text": [{"text": {"content": dados['ass']}}]},
            "INÍCIO DA MISSÃO": {"date": {"start": dados['ini_m'].strftime('%Y-%m-%d')}},
            "FIM DA MISSÃO": {"date": {"start": dados['fim_m'].strftime('%Y-%m-%d')}},
            "STATUS": {"select": {"name": dados['sts']}},
            "DESCRIÇÃO": {"rich_text": [{"text": {"content": dados['obs']}}]}
        }
    }
    # Envia a requisição para o Notion
    response = requests.post(url, headers=headers, json=payload)
    return response.status_code == 200

# --- ESTILO CSS AZUL ROYAL ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(0, 35, 102, 0.85), rgba(0, 35, 102, 0.85)), 
                    url("https://images.unsplash.com/photo-1567899378494-47b22a2ae96a?q=80&w=2070&auto=format&fit=crop");
        background-size: cover; background-attachment: fixed;
    }
    h1, h2, h3, label { color: #00ff41 !important; text-shadow: 2px 2px 4px #000; }
    div.stButton > button:first-child[kind="primary"] { background-color: #28a745 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- NAVEGAÇÃO ---
if "pagina" not in st.session_state: st.session_state.pagina = "🏠 HOME"
if "dados_edicao" not in st.session_state: st.session_state.dados_edicao = None
def navegar(p): st.session_state.pagina = p; st.rerun()

# --- TELAS ---
if st.session_state.pagina == "🏠 HOME":
    if os.path.exists("LOGO.PNG"): st.image("LOGO.PNG", width=250)
    st.title("SISTEMA ZION - GESTÃO")
    c1, c2, c3 = st.columns(3)
    if c1.button("📋 NOVO LANÇAMENTO"): st.session_state.dados_edicao = None; navegar("📋 CADASTRO")
    if c2.button("📊 VER AGENDAMENTOS"): navegar("📊 GRADE")
    if c3.button("💰 FINANCEIRO"): navegar("💰 FINANCEIRO")

elif st.session_state.pagina == "📋 CADASTRO":
    st.header("📋 NOVO REGISTRO DE O.S")
    if st.button("⬅️ VOLTAR"): navegar("🏠 HOME")
    
    with st.form("form_os", clear_on_submit=True):
        c1, c2, c3 = st.columns(3)
        os_n = c1.text_input("Nº O.S")
        dt_s = c2.date_input("DATA SAÍDA")
        cli = c3.text_input("CLIENTE")
        
        c4, c5, c6 = st.columns(3)
        emp = c4.text_input("EMPURRADOR")
        bal = c5.text_input("BALSA")
        ped = c6.text_input("PEDIDO / REF")
        
        c7, c8, c9 = st.columns(3)
        h_e = c7.text_input("HORA EMBARQUE")
        esc1 = c8.text_input("ESCOLTA 1")
        esc2 = c9.text_input("ESCOLTA 2")
        
        c10, c11, c12 = st.columns(3)
        loc = c10.text_input("LOCAL (ORIGEM)")
        dst = c11.text_input("DESTINO")
        ass = c12.text_input("ASSINATURA RESPONSÁVEL")
        
        c13, c14, c15 = st.columns(3)
        ini_m = c13.date_input("INÍCIO MISSÃO")
        fim_m = c14.date_input("FIM MISSÃO")
        sts = c15.selectbox("STATUS", ["Em Andamento", "Encerrado"])
        
        obs = st.text_area("DESCRIÇÃO DETALHADA")
        
        # O BOTÃO QUE EXECUTA A GRAVAÇÃO
        if st.form_submit_button("✅ SALVAR OPERAÇÃO NO NOTION", type="primary"):
            dados_para_salvar = {
                "os_n": os_n, "dt_s": dt_s, "cli": cli, "emp": emp, "bal": bal, "ped": ped,
                "h_e": h_e, "esc1": esc1, "esc2": esc2, "loc": loc, "dst": dst, "ass": ass,
                "ini_m": ini_m, "fim_m": fim_m, "sts": sts, "obs": obs
            }
            if salvar_no_notion(dados_para_salvar):
                st.success("✅ O.S Registrada com sucesso no Notion!")
            else:
                st.error("❌ Erro ao conectar com o Notion. Verifique o Token e ID do Banco.")

# (Restante das telas: Grade e Financeiro seguem a mesma lógica de leitura anterior)
