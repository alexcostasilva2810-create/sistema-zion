import streamlit as st
import requests
import os
import pandas as pd

st.set_page_config(page_title="Zion Tecnologia", layout="wide")

# Conexão Notion
TOKEN = st.secrets["notion"]["token"].replace('"', '').strip()
DATABASE = st.secrets["notion"]["database_id"].replace('"', '').strip()

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

# --- FUNÇÃO DE BUSCA COM PROTEÇÃO (EVITA KEYERROR) ---
def buscar_dados():
    url = f"https://api.notion.com/v1/databases/{DATABASE}/query"
    res = requests.post(url, headers=headers)
    if res.status_code == 200:
        dados = res.json()["results"]
        lista = []
        for pg in dados:
            p = pg["properties"]
            # O uso de .get() evita que o app trave se a coluna não existir
            lista.append({
                "Nº OS": p.get("Nº OS", {}).get("title", [{}])[0].get("text", {}).get("content", ""),
                "DATA INÍCIO": p.get("DATA INÍCIO", {}).get("date", {}).get("start", "") if p.get("DATA INÍCIO") else "",
                "CLIENTE": p.get("CLIENTE", {}).get("rich_text", [{}])[0].get("text", {}).get("content", ""),
                "ESCOLTA 1": p.get("ESCOLTA 1", {}).get("rich_text", [{}])[0].get("text", {}).get("content", ""),
                "ESCOLTA 2": p.get("ESCOLTA 2", {}).get("rich_text", [{}])[0].get("text", {}).get("content", ""),
                "DESTINO": p.get("DESTINO", {}).get("rich_text", [{}])[0].get("text", {}).get("content", "")
            })
        return pd.DataFrame(lista)
    return pd.DataFrame()

# --- NAVEGAÇÃO ---
if "pagina" not in st.session_state:
    st.session_state.pagina = "🏠 HOME"

with st.sidebar:
    if os.path.exists("LOGO.PNG"):
        if st.button("🏠 VOLTAR AO CENTRAL", use_container_width=True):
            st.session_state.pagina = "🏠 HOME"; st.rerun()
        st.image("LOGO.PNG", use_container_width=True)
    menu = st.radio("MENU", ["🏠 HOME", "📋 AGENDAMENTO ZION", "📊 VER AGENDAMENTOS"])
    st.session_state.pagina = menu

# --- TELA DE CONSULTA (TABELA DO VÍDEO) ---
if st.session_state.pagina == "📊 VER AGENDAMENTOS":
    st.header("📊 Operações Realizadas")
    df = buscar_dados()
    if not df.empty:
        # Formata a data para padrão Brasil na visualização
        if "DATA INÍCIO" in df.columns:
            df["DATA INÍCIO"] = pd.to_datetime(df["DATA INÍCIO"]).dt.strftime('%d/%m/%Y')
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.warning("Verifique se as colunas no Notion estão com os nomes corretos.")

# --- TELA DE AGENDAMENTO (SALVAMENTO) ---
elif st.session_state.pagina == "📋 AGENDAMENTO ZION":
    st.header("📋 Cadastro de Operação")
    with st.form("form_cadastro"):
        c1, c2 = st.columns(2)
        os_n = c1.text_input("Nº OS")
        dt_ini = c1.date_input("DATA INÍCIO", format="DD/MM/YYYY")
        cli = c2.text_input("CLIENTE")
        esc1 = c2.text_input("ESCOLTA 1")
        esc2 = st.text_input("ESCOLTA 2")
        
        if st.form_submit_button("✅ SALVAR"):
            payload = {
                "parent": {"database_id": DATABASE},
                "properties": {
                    "Nº OS": {"title": [{"text": {"content": os_n}}]},
                    "DATA INÍCIO": {"date": {"start": str(dt_ini)}},
                    "CLIENTE": {"rich_text": [{"text": {"content": cli}}]},
                    "ESCOLTA 1": {"rich_text": [{"text": {"content": esc1}}]},
                    "ESCOLTA 2": {"rich_text": [{"text": {"content": esc2}}]}
                }
            }
            res = requests.post("https://api.notion.com/v1/pages", headers=headers, json=payload)
            if res.status_code == 200: st.success("🎯 Salvo!")
            else: st.error(f"Erro no Notion: {res.text}")
