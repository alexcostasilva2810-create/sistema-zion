import streamlit as st
import requests
import pandas as pd
import os
from fpdf import FPDF
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

# --- ESTILO CSS AZUL ROYAL FUTURISTA ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(0, 35, 102, 0.88), rgba(0, 35, 102, 0.88)), 
                    url("https://images.unsplash.com/photo-1567899378494-47b22a2ae96a?q=80&w=2070&auto=format&fit=crop");
        background-size: cover; background-position: center; background-attachment: fixed;
    }
    h1, h2, h3, label { color: #00ff41 !important; text-shadow: 2px 2px 4px #000; text-align: center; }
    div.stButton > button:first-child[kind="primary"] { background-color: #28a745 !important; border: none; box-shadow: 0 0 10px #28a745; }
    .stDataFrame { background-color: rgba(15, 23, 42, 0.9); border-radius: 10px; border: 1px solid #00ff41; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNÇÃO CARREGAR DADOS ---
def carregar_dados():
    try:
        res = requests.post(f"https://api.notion.com/v1/databases/{DATABASE}/query", headers=headers)
        if res.status_code == 200:
            results = res.json().get("results", [])
            lista = []
            for r in results:
                p = r["properties"]
                def g_t(n): 
                    try: return p[n]["rich_text"][0]["plain_text"] if p[n]["rich_text"] else ""
                    except: return ""
                def g_d(n): 
                    try: return p[n]["date"]["start"] if p[n]["date"] else None
                    except: return None
                
                status = p["STATUS"]["select"]["name"] if "STATUS" in p and p["STATUS"]["select"] else "Em Andamento"
                valor = 0.0
                if status == "Encerrado":
                    if g_t("ESCOLTA 1"): valor += 1870.0
                    if g_t("ESCOLTA 2"): valor += 970.0

                lista.append({
                    "ID": r["id"],
                    "Nº OS": p["Nº OS"]["title"][0]["plain_text"] if p["Nº OS"]["title"] else "---",
                    "CLIENTE": g_t("CLIENTE"), "DT_SAIDA_RAW": g_d("DT SAÍDA"),
                    "DT SAÍDA": datetime.strptime(g_d("DT SAÍDA"), '%Y-%m-%d').strftime('%d/%m/%Y') if g_d("DT SAÍDA") else "---",
                    "EMPURRADOR": g_t("EMPURRADOR"), "BALSA": g_t("BALSA"),
                    "LOCAL": g_t("LOCAL"), "DESTINO": g_t("DESTINO"),
                    "HORA_EMBARQUE": g_t("HORA DE EMBARQUE"),
                    "ESCOLTA 1": g_t("ESCOLTA 1"), "ESCOLTA 2": g_t("ESCOLTA 2"),
                    "DESCRIÇÃO": g_t("DESCRIÇÃO"), "PEDIDO": g_t("PEDIDO"),
                    "INICIO_MISSAO": g_d("INÍCIO DA MISSÃO"), "FIM_MISSAO": g_d("FIM DA MISSÃO"),
                    "ASSINATURA": g_t("ASSINATURA RESPONSÁVEL"), "STATUS": status, "VALOR": valor
                })
            return lista
    except: return []

# --- FUNÇÃO SALVAR NO NOTION ---
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
    res = requests.post(url, headers=headers, json=payload)
    return res.status_code == 200

# --- NAVEGAÇÃO ---
if "pagina" not in st.session_state: st.session_state.pagina = "🏠 HOME"
if "dados_edicao" not in st.session_state: st.session_state.dados_edicao = None
def navegar(p): st.session_state.pagina = p; st.rerun()

# --- TELA HOME ---
if st.session_state.pagina == "🏠 HOME":
    st.markdown("<br>", unsafe_allow_html=True)
    if os.path.exists("LOGO.PNG"): st.image("LOGO.PNG", width=250)
    st.markdown("<h1>SISTEMA ZION</h1><h3>OPERACIONAL & FINANCEIRO</h3>", unsafe_allow_html=True)
    st.markdown("<br><hr><br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    if c1.button("📋 NOVO LANÇAMENTO"): st.session_state.dados_edicao = None; navegar("📋 CADASTRO")
    if c2.button("📊 VER AGENDAMENTOS"): navegar("📊 GRADE")
    if c3.button("💰 FINANCEIRO"): navegar("💰 FINANCEIRO")

# --- TELA CADASTRO (17 CAMPOS) ---
elif st.session_state.pagina == "📋 CADASTRO":
    st.markdown("## 📋 REGISTRO DE O.S")
    if st.button("⬅️ VOLTAR"): navegar("🏠 HOME")
    with st.form("form_os"):
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
        obs = st.text_area("DESCRIÇÃO")
        if st.form_submit_button("✅ SALVAR OPERAÇÃO", type="primary"):
            dados = {"os_n":os_n, "dt_s":dt_s, "cli":cli, "emp":emp, "bal":bal, "ped":ped, "h_e":h_e, "esc1":esc1, "esc2":esc2, "loc":loc, "dst":dst, "ass":ass, "ini_m":ini_m, "fim_m":fim_m, "sts":sts, "obs":obs}
            if salvar_no_notion(dados): st.success("Salvo!"); navegar("📊 GRADE")
            else: st.error("Erro ao salvar!")

# --- TELA GRADE (RESTAURADA) ---
elif st.session_state.pagina == "📊 GRADE":
    st.markdown("## 📊 GRADE DE AGENDAMENTOS")
    if st.button("⬅️ VOLTAR"): navegar("🏠 HOME")
    dados = carregar_dados()
    if dados:
        df = pd.DataFrame(dados)
        st.dataframe(df[["Nº OS", "CLIENTE", "DT SAÍDA", "EMPURRADOR", "BALSA", "STATUS"]], use_container_width=True)
        for d in dados:
            with st.expander(f"OPÇÕES O.S {d['Nº OS']}"):
                st.write(f"Cliente: {d['CLIENTE']} | Status: {d['STATUS']}")
                if st.button("✏️ EDITAR", key=f"ed_{d['ID']}", type="primary"): 
                    st.session_state.dados_edicao = d; navegar("📋 CADASTRO")

# --- TELA FINANCEIRO (RESTAURADA) ---
elif st.session_state.pagina == "💰 FINANCEIRO":
    st.markdown("## 💰 FINANCEIRO")
    if st.button("⬅️ VOLTAR"): navegar("🏠 HOME")
    c1, c2 = st.columns(2)
    ini_f = c1.date_input("INÍCIO", format="DD/MM/YYYY")
    fim_f = c2.date_input("FIM", format="DD/MM/YYYY")
    dados = carregar_dados()
    if dados:
        df = pd.DataFrame(dados)
        df['dt_f'] = pd.to_datetime(df['DT_SAIDA_RAW'])
        df_filt = df[(df['dt_f'] >= pd.Timestamp(ini_f)) & (df['dt_f'] <= pd.Timestamp(fim_f))]
        st.metric("TOTAL NO PERÍODO", f"R$ {df_filt['VALOR'].sum():,.2f}")
        st.dataframe(df_filt[["Nº OS", "CLIENTE", "DT SAÍDA", "VALOR"]], use_container_width=True)
