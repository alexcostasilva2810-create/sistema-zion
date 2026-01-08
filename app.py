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

# --- ESTILO CSS AZUL ROYAL (TRAVADO) ---
st.markdown("""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
    /* Fundo Business Premium */
    .stApp {
        background: linear-gradient(rgba(0, 20, 60, 0.85), rgba(0, 20, 60, 0.85)), 
                    url("https://images.unsplash.com/photo-1454165205744-3b78555e5572?q=80&w=2070&auto=format&fit=crop");
        background-size: cover; background-position: center; background-attachment: fixed;
    }
    
    h1 { color: #ffffff !important; font-weight: 800; letter-spacing: 2px; text-transform: uppercase; text-align: center; margin-top: 20px;}

    /* Cards Business */
    div.stButton > button {
        width: 100%;
        height: 150px !important;
        background: rgba(255, 255, 255, 0.05) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 20px !important;
        transition: all 0.4s ease-in-out !important;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3) !important;
    }

    div.stButton > button:hover {
        background: rgba(255, 255, 255, 0.12) !important;
        border-color: #00ff41 !important;
        transform: translateY(-8px) !important;
    }

    .icon-container {
        font-size: 40px;
        color: #00ff41;
        text-align: center;
        display: block;
        margin-bottom: 5px;
    }

    /* Container da Logo abaixo dos ícones */
    .logo-footer {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-top: 50px;
        padding: 20px;
    }

    .logo-img {
        width: 250px; /* Ajuste o tamanho da sua logo aqui */
        filter: drop-shadow(0px 5px 15px rgba(0,0,0,0.5));
        opacity: 0.9;
    }
    </style>
    """, unsafe_allow_html=True)# --- FUNÇÃO CARREGAR DADOS ---
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
                valor_os = 0.0
                try: valor_os = p["VALOR TOTAL"]["number"] if p["VALOR TOTAL"]["number"] else 0.0
                except: valor_os = 0.0

                lista.append({
                    "ID": r["id"],
                    "Nº OS": p["Nº OS"]["title"][0]["plain_text"] if p["Nº OS"]["title"] else "---",
                    "CLIENTE": g_t("CLIENTE"), 
                    "DT SAÍDA": datetime.strptime(g_d("DT SAÍDA"), '%Y-%m-%d').strftime('%d/%m/%Y') if g_d("DT SAÍDA") else "---",
                    "DT_RAW": g_d("DT SAÍDA"),
                    "EMPURRADOR": g_t("EMPURRADOR"), "BALSA": g_t("BALSA"),
                    "PEDIDO": g_t("PEDIDO"), "HORA_EMBARQUE": g_t("HORA DE EMBARQUE"),
                    "ESCOLTA 1": g_t("ESCOLTA 1"), "ESCOLTA 2": g_t("ESCOLTA 2"),
                    "LOCAL": g_t("LOCAL"), "DESTINO": g_t("DESTINO"),
                    "ASSINATURA": g_t("ASSINATURA RESPONSÁVEL"),
                    "STATUS": status, "VALOR": valor_os
                })
            return lista
    except: return []

# --- FUNÇÃO SALVAR NO NOTION (17 COLUNAS) ---
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
            "ASSINATURA RESPONSÁVEL": {"rich_text": [{"text": {"content": str(d['ass'])}}]},
            "INÍCIO DA MISSÃO": {"date": {"start": d['ini_m'].strftime('%Y-%m-%d')}},
            "FIM DA MISSÃO": {"date": {"start": d['fim_m'].strftime('%Y-%m-%d')}},
            "STATUS": {"select": {"name": str(d['sts'])}},
            "DESCRIÇÃO": {"rich_text": [{"text": {"content": str(d['obs'])}}]},
            "VALOR TOTAL": {"number": float(d['v_total']) if d['v_total'] else 0.0}
        }
    }
    res = requests.post(url, headers=headers, json=payload)
    return res.status_code == 200

# --- NAVEGAÇÃO ---
if "pagina" not in st.session_state: st.session_state.pagina = "🏠 HOME"
def navegar(p): st.session_state.pagina = p; st.rerun()

#---- Tela Inicial ----# 
#---- Tela Inicial ----# 
if st.session_state.pagina == "🏠 HOME":
    st.markdown("<h1>ZION BUSINESS TECHNOLOGY</h1>", unsafe_allow_html=True)
    
    # Grid de Navegação
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.markdown('<i class="fas fa-file-signature icon-container"></i>', unsafe_allow_html=True)
        if st.button("NOVO LANÇAMENTO"): navegar("📋 CADASTRO")
        
    with c2:
        st.markdown('<i class="fas fa-layer-group icon-container"></i>', unsafe_allow_html=True)
        if st.button("GRADE DE OPERAÇÕES"): navegar("📊 GRADE")
        
    with c3:
        st.markdown('<i class="fas fa-chart-pie icon-container"></i>', unsafe_allow_html=True)
        if st.button("INTELIGÊNCIA FINANCEIRA"): navegar("💰 FINANCEIRO")

    # --- LOGO ABAIXO DOS ÍCONES ---
    st.markdown("""
        <div class="logo-footer">
            <img src="https://i.imgur.com/vHq0AUP.png" class="logo-img" alt="Logo Zion">
        </div>
    """, unsafe_allow_html=True)

#---- Tela Cadastro ----# 
elif st.session_state.pagina == "📋 CADASTRO":
    st.header("📋 NOVO REGISTRO (17 COLUNAS)")
    if st.button("⬅️ VOLTAR"): navegar("🏠 HOME")
    with st.form("form_os"):
        c1, c2, c3 = st.columns(3)
        os_n, dt_s, cli = c1.text_input("Nº O.S"), c2.date_input("DATA SAÍDA", format="DD/MM/YYYY"), c3.text_input("CLIENTE")
        c4, c5, c6 = st.columns(3)
        emp, bal, ped = c4.text_input("EMPURRADOR"), c5.text_input("BALSA"), c6.text_input("PEDIDO")
        c7, c8, c9 = st.columns(3)
        h_e, esc1, esc2 = c7.text_input("HORA EMBARQUE"), c8.text_input("ESCOLTA 1"), c9.text_input("ESCOLTA 2")
        c10, c11, c12 = st.columns(3)
        loc, dst, ass = c10.text_input("LOCAL"), c11.text_input("DESTINO"), c12.text_input("ASSINATURA RESP.")
        c13, c14, c15 = st.columns(3)
        ini_m, fim_m, sts = c13.date_input("INÍCIO MISSÃO", format="DD/MM/YYYY"), c14.date_input("FIM MISSÃO", format="DD/MM/YYYY"), c15.selectbox("STATUS", ["Em Andamento", "Encerrado"])
        c16, c17 = st.columns([2, 1])
        obs, v_total = c16.text_area("DESCRIÇÃO"), c17.text_input("VALOR TOTAL", value="0.0")
        
        if st.form_submit_button("✅ SALVAR OPERAÇÃO", type="primary"):
            d = {"os_n":os_n, "dt_s":dt_s, "cli":cli, "emp":emp, "bal":bal, "ped":ped, "h_e":h_e, "esc1":esc1, "esc2":esc2, "loc":loc, "dst":dst, "ass":ass, "ini_m":ini_m, "fim_m":fim_m, "sts":sts, "obs":obs, "v_total":v_total}
            if salvar_no_notion(d): navegar("📊 GRADE")
            else: st.error("Erro ao salvar no Notion.")

#---- Tela Grade ----# 
elif st.session_state.pagina == "📊 GRADE":
    st.header("📊 AGENDAMENTOS")
    if st.button("⬅️ VOLTAR"): navegar("🏠 HOME")
    dados = carregar_dados()
    df = pd.DataFrame(dados) if dados else pd.DataFrame(columns=["Nº OS", "CLIENTE", "DT SAÍDA", "STATUS"])
    st.dataframe(df[["Nº OS", "CLIENTE", "DT SAÍDA", "EMPURRADOR", "BALSA", "STATUS"]], use_container_width=True)
    for d in (dados or []):
        with st.expander(f"Ações O.S {d['Nº OS']}"):
            c1, c2 = st.columns(2)
            c1.button("✏️ EDITAR", key=f"ed_{d['ID']}")
            c2.button("📄 PDF", key=f"pdf_{d['ID']}")

#---- Tela Financeiro ----# 
elif st.session_state.pagina == "💰 FINANCEIRO":
    st.header("💰 FINANCEIRO")
    if st.button("⬅️ VOLTAR"): navegar("🏠 HOME")
    c1, c2 = st.columns(2)
    i_f, f_f = c1.date_input("INÍCIO", format="DD/MM/YYYY"), c2.date_input("FIM", format="DD/MM/YYYY")
    dados = carregar_dados()
    if dados:
        df = pd.DataFrame(dados)
        df['dt_p'] = pd.to_datetime(df['DT_RAW'])
        df_f = df[(df['dt_p'] >= pd.Timestamp(i_f)) & (df['dt_p'] <= pd.Timestamp(f_f))]
        st.metric("FATURAMENTO", f"R$ {df_f['VALOR'].sum():,.2f}")
        st.dataframe(df_f[["Nº OS", "CLIENTE", "DT SAÍDA", "EMPURRADOR", "BALSA", "ESCOLTA 1", "ESCOLTA 2", "VALOR"]], use_container_width=True)
    else: st.dataframe(pd.DataFrame(columns=["Nº OS", "CLIENTE", "DT SAÍDA", "VALOR"]), use_container_width=True)
