import streamlit as st
import requests
import pandas as pd
import os
from datetime import datetime

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Zion Tecnologia - Gestão O.S", layout="wide")

# --- CONEXÃO NOTION ---
TOKEN = st.secrets["notion"]["token"].replace('"', '').strip()
DATABASE = st.secrets["notion"]["database_id"].replace('"', '').strip()

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

# --- ESTILO CSS AZUL ROYAL ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(0, 35, 102, 0.88), rgba(0, 35, 102, 0.88)), 
                    url("https://images.unsplash.com/photo-1567899378494-47b22a2ae96a?q=80&w=2070&auto=format&fit=crop");
        background-size: cover; background-position: center; background-attachment: fixed;
    }
    h1, h2, h3, label { color: #00ff41 !important; text-shadow: 2px 2px 4px #000; text-align: center; }
    div.stButton > button:first-child[kind="primary"] { background-color: #28a745 !important; border: none; width: 100%; height: 50px; font-weight: bold; }
    .stDataFrame { background-color: rgba(15, 23, 42, 0.9); border: 1px solid #00ff41; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNÇÃO SALVAR NO NOTION (AS 17 COLUNAS) ---
def salvar_no_notion(d):
    url = "https://api.notion.com/v1/pages"
    payload = {
        "parent": {"database_id": DATABASE},
        "properties": {
            "Nº OS": {"title": [{"text": {"content": str(d['os_n'])}}]},
            "CLIENTE": {"rich_text": [{"text": {"content": str(d['cli'])}}]},
            "DT SAÍDA": {"date": {"start": d['dt_s'].strftime('%Y-%m-%d')}},
            "EMPURRADOR": {"rich_text": [{"text": {"content": str(d['emp'])}}]},
            "BALSA": {"rich_text": [{"text": {"content": str(d['bal'])}}]},
            "PEDIDO": {"rich_text": [{"text": {"content": str(d['ped'])}}]},
            "HORA DE EMBARQUE": {"rich_text": [{"text": {"content": str(d['h_e'])}}]},
            "ESCOLTA 1": {"rich_text": [{"text": {"content": str(d['esc1'])}}]},
            "ESCOLTA 2": {"rich_text": [{"text": {"content": str(d['esc2'])}}]},
            "LOCAL": {"rich_text": [{"text": {"content": str(d['loc'])}}]},
            "DESTINO": {"rich_text": [{"text": {"content": str(d['dst'])}}]},
            "ASSINATURA": {"rich_text": [{"text": {"content": str(d['ass'])}}]},
            "INÍCIO DA MISSÃO": {"date": {"start": d['ini_m'].strftime('%Y-%m-%d')}},
            "FIM DA MISSÃO": {"date": {"start": d['fim_m'].strftime('%Y-%m-%d')}},
            "STATUS": {"select": {"name": str(d['sts'])}},
            "DESCRIÇÃO": {"rich_text": [{"text": {"content": str(d['obs'])}}]},
            "VALOR": {"number": float(d['v_total']) if d['v_total'] else 0.0} # 17ª Coluna (Financeira)
        }
    }
    res = requests.post(url, headers=headers, json=payload)
    if res.status_code != 200:
        st.error(f"Erro Notion: {res.json().get('message')}")
    return res.status_code == 200

# --- NAVEGAÇÃO ---
if "pagina" not in st.session_state: st.session_state.pagina = "🏠 HOME"
def navegar(p): st.session_state.pagina = p; st.rerun()

# --- TELAS ---
if st.session_state.pagina == "🏠 HOME":
    st.markdown("<h1>SISTEMA ZION - GESTÃO MARÍTIMA</h1>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    if c1.button("📋 NOVO LANÇAMENTO"): navegar("📋 CADASTRO")
    if c2.button("📊 VER AGENDAMENTOS"): navegar("📊 GRADE")
    if c3.button("💰 FINANCEIRO"): navegar("💰 FINANCEIRO")

elif st.session_state.pagina == "📋 CADASTRO":
    st.markdown("## 📋 CADASTRO COMPLETO DE O.S (17 COLUNAS)")
    if st.button("⬅️ VOLTAR"): navegar("🏠 HOME")
    
    with st.form("form_os"):
        # LINHA 1
        c1, c2, c3 = st.columns(3)
        os_n = c1.text_input("1. Nº O.S")
        dt_s = c2.date_input("2. DATA SAÍDA", format="DD/MM/YYYY")
        cli = c3.text_input("3. CLIENTE")
        
        # LINHA 2
        c4, c5, c6 = st.columns(3)
        emp = c4.text_input("4. EMPURRADOR")
        bal = c5.text_input("5. BALSA")
        ped = c6.text_input("6. PEDIDO")
        
        # LINHA 3
        c7, c8, c9 = st.columns(3)
        h_e = c7.text_input("7. HORA DE EMBARQUE")
        esc1 = c8.text_input("8. ESCOLTA 1")
        esc2 = c9.text_input("9. ESCOLTA 2")
        
        # LINHA 4
        c10, c11, c12 = st.columns(3)
        loc = c10.text_input("10. LOCAL")
        dst = c11.text_input("11. DESTINO")
        ass = c12.text_input("12. ASSINATURA RESPONSÁVEL")
        
        # LINHA 5
        c13, c14, c15 = st.columns(3)
        ini_m = c13.date_input("13. INÍCIO DA MISSÃO", format="DD/MM/YYYY")
        fim_m = c14.date_input("14. FIM DA MISSÃO", format="DD/MM/YYYY")
        sts = c15.selectbox("15. STATUS", ["Em Andamento", "Encerrado"])
        
        # LINHA 6
        c16, c17 = st.columns([2, 1])
        obs = c16.text_area("16. DESCRIÇÃO / OBSERVAÇÕES")
        v_total = c17.text_input("17. VALOR TOTAL (R$)", value="0.00")
        
        if st.form_submit_button("✅ SALVAR REGISTRO COMPLETO", type="primary"):
            dados = {
                "os_n":os_n, "dt_s":dt_s, "cli":cli, "emp":emp, "bal":bal, "ped":ped,
                "h_e":h_e, "esc1":esc1, "esc2":esc2, "loc":loc, "dst":dst, "ass":ass,
                "ini_m":ini_m, "fim_m":fim_m, "sts":sts, "obs":obs, "v_total":v_total
            }
            if salvar_no_notion(dados):
                st.success("Tudo certo! Lançamento realizado.")
                navegar("📊 GRADE")

elif st.session_state.pagina == "📊 GRADE":
    st.markdown("## 📊 AGENDAMENTOS")
    if st.button("⬅️ VOLTAR"): navegar("🏠 HOME")
    # Lógica de carregamento de dados mantida para exibir a grade...

elif st.session_state.pagina == "💰 FINANCEIRO":
    st.markdown("## 💰 FINANCEIRO")
    if st.button("⬅️ VOLTAR"): navegar("🏠 HOME")
    # Lógica financeira mantida...
