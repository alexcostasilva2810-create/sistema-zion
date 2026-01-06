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
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

# --- ESTILO CSS ---
st.markdown("""
    <style>
    div.stButton > button:first-child[kind="primary"] { background-color: #28a745 !important; color: white !important; }
    .stButton>button { width: 100%; border-radius: 8px; font-weight: bold; height: 3.5em; }
    [data-testid="stMetricValue"] { font-size: 1.5rem; color: #28a745; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNÇÃO CARREGAR DADOS (TODAS AS COLUNAS) ---
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
                    try: return datetime.strptime(p[n]["date"]["start"], '%Y-%m-%d').strftime('%d/%m/%Y') if p[n]["date"] else ""
                    except: return ""
                
                status = p["STATUS"]["select"]["name"] if "STATUS" in p and p["STATUS"]["select"] else "Em Andamento"
                
                # Regra de Cálculo Financeiro
                valor = 0.0
                if status == "Encerrado":
                    # Lógica: Escolta (1870) + Vigilante (970) se preenchidos
                    if g_t("ESCOLTA 1"): valor += 1870.0
                    if g_t("ESCOLTA 2"): valor += 970.0 # Assumindo 2º como vigilante ou conforme sua regra

                lista.append({
                    "ID": r["id"],
                    "Nº OS": p["Nº OS"]["title"][0]["plain_text"] if p["Nº OS"]["title"] else "---",
                    "CLIENTE": g_t("CLIENTE"), "DT SAÍDA": g_d("DT SAÍDA"),
                    "EMPURRADOR": g_t("EMPURRADOR"), "BALSA": g_t("BALSA"),
                    "LOCAL": g_t("LOCAL"), "DESTINO": g_t("DESTINO"),
                    "HORA_EMBARQUE": g_t("HORA DE EMBARQUE"),
                    "ESCOLTA 1": g_t("ESCOLTA 1"), "ESCOLTA 2": g_t("ESCOLTA 2"),
                    "DESCRIÇÃO": g_t("DESCRIÇÃO"), "PEDIDO": g_t("PEDIDO"),
                    "INÍCIO": g_d("INÍCIO DA MISSÃO"), "FIM": g_d("FIM DA MISSÃO"),
                    "ASSINATURA": g_t("ASSINATURA RESPONSÁVEL"),
                    "STATUS": status,
                    "VALOR_TOTAL": valor
                })
            return lista
    except: return []
    return []

# --- NAVEGAÇÃO ---
if "pagina" not in st.session_state: st.session_state.pagina = "🏠 HOME"
if "dados_edicao" not in st.session_state: st.session_state.dados_edicao = None
def navegar(p): st.session_state.pagina = p; st.rerun()

# --- TELA HOME ---
if st.session_state.pagina == "🏠 HOME":
    if os.path.exists("LOGO.PNG"): st.image("LOGO.PNG", width=250)
    st.title("🛡️ Zion Tecnologia - Gestão Transdourada")
    st.markdown("---")
    c1, c2, c3 = st.columns(3)
    if c1.button("📋 NOVO LANÇAMENTO"): st.session_state.dados_edicao = None; navegar("📋 CADASTRO")
    if c2.button("📊 VER AGENDAMENTOS"): navegar("📊 GRADE")
    if c3.button("💰 FINANCEIRO"): navegar("💰 FINANCEIRO")

# --- TELA CADASTRO (RESTAURADA COM 17 CAMPOS) ---
elif st.session_state.pagina == "📋 CADASTRO":
    edit = st.session_state.dados_edicao
    st.header("📝 Registro de Ordem de Serviço")
    if st.button("⬅️ VOLTAR"): navegar("🏠 HOME")
    
    with st.form("form_os"):
        c1, c2, c3 = st.columns(3)
        os_n = c1.text_input("Nº O.S", value=edit["Nº OS"] if edit else "")
        dt_s = c2.date_input("DATA SAÍDA")
        cli = c3.text_input("CLIENTE", value=edit["CLIENTE"] if edit else "")
        
        c4, c5, c6 = st.columns(3)
        ini = c4.date_input("INÍCIO MISSÃO")
        fim = c5.date_input("FIM MISSÃO")
        bal = c6.text_input("BALSA", value=edit["BALSA"] if edit else "")
        
        c7, c8, c9 = st.columns(3)
        h_e = c7.text_input("HORA EMBARQUE", value=edit.get("HORA_EMBARQUE", "") if edit else "")
        esc1 = c8.text_input("ESCOLTA 1 (Vlr: 1870)", value=edit.get("ESCOLTA 1", "") if edit else "")
        esc2 = c9.text_input("ESCOLTA 2 (Vlr: 970)", value=edit.get("ESCOLTA 2", "") if edit else "")
        
        c10, c11, c12 = st.columns(3)
        loc = c10.text_input("LOCAL (ORIGEM)", value=edit.get("LOCAL", "") if edit else "")
        dst = c11.text_input("DESTINO", value=edit.get("DESTINO", "") if edit else "")
        ped = c12.text_input("PEDIDO / REF", value=edit.get("PEDIDO", "") if edit else "")
        
        c13, c14, c15 = st.columns(3)
        emp = c13.text_input("EMPURRADOR", value=edit.get("EMPURRADOR", "") if edit else "")
        ass = c14.text_input("ASSINATURA RESPONSÁVEL", value=edit.get("ASSINATURA", "") if edit else "")
        sts = c15.selectbox("STATUS", ["Em Andamento", "Encerrado"])
        
        obs = st.text_area("DESCRIÇÃO DETALHADA", value=edit.get("DESCRIÇÃO", "") if edit else "")
        
        if st.form_submit_button("✅ SALVAR OPERAÇÃO", type="primary"):
            payload = {"properties": {
                "Nº OS": {"title": [{"text": {"content": str(os_n)}}]},
                "CLIENTE": {"rich_text": [{"text": {"content": cli}}]},
                "DT SAÍDA": {"date": {"start": dt_s.strftime('%Y-%m-%d')}},
                "INÍCIO DA MISSÃO": {"date": {"start": ini.strftime('%Y-%m-%d')}},
                "FIM DA MISSÃO": {"date": {"start": fim.strftime('%Y-%m-%d')}},
                "EMPURRADOR": {"rich_text": [{"text": {"content": emp}}]},
                "BALSA": {"rich_text": [{"text": {"content": bal}}]},
                "LOCAL": {"rich_text": [{"text": {"content": loc}}]},
                "DESTINO": {"rich_text": [{"text": {"content": dst}}]},
                "HORA DE EMBARQUE": {"rich_text": [{"text": {"content": h_e}}]},
                "ESCOLTA 1": {"rich_text": [{"text": {"content": esc1}}]},
                "ESCOLTA 2": {"rich_text": [{"text": {"content": esc2}}]},
                "PEDIDO": {"rich_text": [{"text": {"content": ped}}]},
                "ASSINATURA RESPONSÁVEL": {"rich_text": [{"text": {"content": ass}}]},
                "DESCRIÇÃO": {"rich_text": [{"text": {"content": obs}}]},
                "STATUS": {"select": {"name": sts}}
            }}
            url = f"https://api.notion.com/v1/pages/{edit['ID']}" if edit else "https://api.notion.com/v1/pages"
            if not edit: payload["parent"] = {"database_id": DATABASE}
            res = requests.patch(url, headers=headers, json=payload) if edit else requests.post(url, headers=headers, json=payload)
            if res.status_code == 200:
                st.success("🎯 Dados integrados ao Notion!"); navegar("📊 GRADE")

# --- TELA GRADE ---
elif st.session_state.pagina == "📊 GRADE":
    st.header("📊 Grade de Agendamentos")
    if st.button("⬅️ VOLTAR"): navegar("🏠 HOME")
    dados = carregar_dados()
    if dados:
        df = pd.DataFrame(dados)
        st.dataframe(df[["Nº OS", "CLIENTE", "EMPURRADOR", "BALSA", "STATUS"]], use_container_width=True)
        for d in dados:
            with st.expander(f"Ações: O.S {d['Nº OS']} - {d['CLIENTE']}"):
                if st.button("✏️ EDITAR REGISTRO", key=f"ed_{d['ID']}"):
                    st.session_state.dados_edicao = d; navegar("📋 CADASTRO")
    else: st.warning("Sem dados.")

# --- TELA FINANCEIRO (COM CÁLCULOS RESTAURADA) ---
elif st.session_state.pagina == "💰 FINANCEIRO":
    st.header("💰 Painel Financeiro Zion")
    if st.button("⬅️ VOLTAR"): navegar("🏠 HOME")
    dados = carregar_dados()
    if dados:
        df = pd.DataFrame(dados)
        total_geral = df["VALOR_TOTAL"].sum()
        st.metric("FATURAMENTO TOTAL (O.S ENCERRADAS)", f"R$ {total_geral:,.2f}")
        
        # Tabela formatada para o financeiro
        df_fin = df[df["VALOR_TOTAL"] > 0][["Nº OS", "CLIENTE", "DT SAÍDA", "VALOR_TOTAL"]]
        st.subheader("Operações para Faturamento")
        st.table(df_fin)
    else: st.info("Nenhuma operação encerrada com valores para exibir.")
