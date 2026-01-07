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
    div.stButton > button:first-child[kind="primary"] { background-color: #28a745 !important; border: none; }
    .stDataFrame { background-color: rgba(15, 23, 42, 0.9); border: 1px solid #00ff41; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNÇÃO SALVAR (FOCO NA COLUNA PEDIDO) ---
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
            # ATENÇÃO: Verifique se no Notion o nome é exatamente PEDIDO (Maiúsculo)
            "PEDIDO": {"rich_text": [{"text": {"content": str(d['ped'])}}]},
            "HORA DE EMBARQUE": {"rich_text": [{"text": {"content": str(d['h_e'])}}]},
            "ESCOLTA 1": {"rich_text": [{"text": {"content": str(d['esc1'])}}]},
            "ESCOLTA 2": {"rich_text": [{"text": {"content": str(d['esc2'])}}]},
            "LOCAL": {"rich_text": [{"text": {"content": str(d['loc'])}}]},
            "DESTINO": {"rich_text": [{"text": {"content": str(d['dst'])}}]},
            "ASSINATURA RESPONSÁVEL": {"rich_text": [{"text": {"content": str(d['ass'])}}]},
            "INÍCIO DA MISSÃO": {"date": {"start": d['ini_m'].strftime('%Y-%m-%d')}},
            "FIM DA MISSÃO": {"date": {"start": d['fim_m'].strftime('%Y-%m-%d')}},
            "STATUS": {"select": {"name": str(d['sts'])}},
            "DESCRIÇÃO": {"rich_text": [{"text": {"content": str(d['obs'])}}]}
        }
    }
    res = requests.post(url, headers=headers, json=payload)
    if res.status_code != 200:
        # Isso vai nos mostrar no Streamlit exatamente qual o erro que o Notion está dando
        st.error(f"Erro do Notion: {res.json().get('message', 'Erro desconhecido')}")
    return res.status_code == 200

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
                lista.append({
                    "Nº OS": p["Nº OS"]["title"][0]["plain_text"] if p["Nº OS"]["title"] else "---",
                    "CLIENTE": g_t("CLIENTE"), 
                    "DT SAÍDA": datetime.strptime(g_d("DT SAÍDA"), '%Y-%m-%d').strftime('%d/%m/%Y') if g_d("DT SAÍDA") else "---",
                    "DT_RAW": g_d("DT SAÍDA"),
                    "EMPURRADOR": g_t("EMPURRADOR"), "BALSA": g_t("BALSA"), "STATUS": status,
                    "VALOR": 1870.0 if status == "Encerrado" else 0.0
                })
            return lista
    except: return []

# --- NAVEGAÇÃO ---
if "pagina" not in st.session_state: st.session_state.pagina = "🏠 HOME"
def navegar(p): st.session_state.pagina = p; st.rerun()

# --- TELAS ---
if st.session_state.pagina == "🏠 HOME":
    if os.path.exists("LOGO.PNG"): st.image("LOGO.PNG", width=250)
    st.markdown("<h1>SISTEMA ZION</h1>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    if c1.button("📋 NOVO LANÇAMENTO"): navegar("📋 CADASTRO")
    if c2.button("📊 VER AGENDAMENTOS"): navegar("📊 GRADE")
    if c3.button("💰 FINANCEIRO"): navegar("💰 FINANCEIRO")

elif st.session_state.pagina == "📋 CADASTRO":
    st.header("📋 NOVO REGISTRO")
    if st.button("⬅️ VOLTAR"): navegar("🏠 HOME")
    with st.form("form_os"):
        c1, c2, c3 = st.columns(3)
        os_n = c1.text_input("Nº O.S")
        dt_s = c2.date_input("DATA SAÍDA", format="DD/MM/YYYY")
        cli = c3.text_input("CLIENTE")
        c4, c5, c6 = st.columns(3)
        emp = c4.text_input("EMPURRADOR")
        bal = c5.text_input("BALSA")
        ped = c6.text_input("PEDIDO") 
        c7, c8, c9 = st.columns(3)
        h_e = c7.text_input("HORA EMBARQUE")
        esc1 = c8.text_input("ESCOLTA 1")
        esc2 = c9.text_input("ESCOLTA 2")
        c10, c11, c12 = st.columns(3)
        loc = c10.text_input("LOCAL (ORIGEM)")
        dst = c11.text_input("DESTINO")
        ass = c12.text_input("ASSINATURA RESPONSÁVEL")
        c13, c14, c15 = st.columns(3)
        ini_m = c13.date_input("INÍCIO MISSÃO", format="DD/MM/YYYY")
        fim_m = c14.date_input("FIM MISSÃO", format="DD/MM/YYYY")
        sts = c15.selectbox("STATUS", ["Em Andamento", "Encerrado"])
        obs = st.text_area("DESCRIÇÃO")
        
        if st.form_submit_button("✅ SALVAR OPERAÇÃO", type="primary"):
            dados = {"os_n":os_n, "dt_s":dt_s, "cli":cli, "emp":emp, "bal":bal, "ped":ped, "h_e":h_e, "esc1":esc1, "esc2":esc2, "loc":loc, "dst":dst, "ass":ass, "ini_m":ini_m, "fim_m":fim_m, "sts":sts, "obs":obs}
            if salvar_no_notion(dados): 
                st.success("Salvo com sucesso!")
                navegar("📊 GRADE")

elif st.session_state.pagina == "📊 GRADE":
    st.header("📊 AGENDAMENTOS")
    if st.button("⬅️ VOLTAR"): navegar("🏠 HOME")
    dados = carregar_dados()
    cols = ["Nº OS", "CLIENTE", "DT SAÍDA", "EMPURRADOR", "BALSA", "STATUS"]
    df = pd.DataFrame(dados) if dados else pd.DataFrame(columns=cols)
    st.dataframe(df[cols], use_container_width=True)

elif st.session_state.pagina == "💰 FINANCEIRO":
    st.header("💰 FINANCEIRO")
    if st.button("⬅️ VOLTAR"): navegar("🏠 HOME")
    c1, c2 = st.columns(2)
    i_f, f_f = c1.date_input("INÍCIO", format="DD/MM/YYYY"), c2.date_input("FIM", format="DD/MM/YYYY")
    dados = carregar_dados()
    cols_fin = ["Nº OS", "CLIENTE", "DT SAÍDA", "VALOR"]
    if dados:
        df = pd.DataFrame(dados)
        df['dt_p'] = pd.to_datetime(df['DT_RAW'])
        df_f = df[(df['dt_p'] >= pd.Timestamp(i_f)) & (df['dt_p'] <= pd.Timestamp(f_f))]
        st.metric("TOTAL NO PERÍODO", f"R$ {df_f['VALOR'].sum():,.2f}")
        st.dataframe(df_f[cols_fin], use_container_width=True)
    else: st.dataframe(pd.DataFrame(columns=cols_fin), use_container_width=True)
