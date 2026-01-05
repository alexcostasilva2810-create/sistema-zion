import streamlit as st
import requests

st.set_page_config(page_title="Zion Tecnologia", layout="wide")

# Puxando os dados que você salvou nos Secrets
NOTION_TOKEN = st.secrets["notion"]["token"]
DATABASE_ID = st.secrets["notion"]["database_id"]

headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

st.title("🚨 Agendamento Zion")

with st.form("form_agendamento", clear_on_submit=True):
    col1, col2 = st.columns(2)
    with col1:
        os_num = st.text_input("Nº OS")
        cliente = st.text_input("CLIENTE")
    with col2:
        data_ini = st.date_input("DATA")
        hora_ini = st.text_input("HORA (ex: 0800)")

    submit = st.form_submit_button("✅ SALVAR OPERAÇÃO")

    if submit:
        url = "https://api.notion.com/v1/pages"
        payload = {
            "parent": {"database_id": DATABASE_ID},
            "properties": {
                "Nº OS": {"title": [{"text": {"content": os_num}}]},
                "CLIENTE": {"rich_text": [{"text": {"content": cliente}}]},
                "INÍCIO": {"rich_text": [{"text": {"content": f"{data_ini} {hora_ini}"}}]}
            }
        }
        
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code == 200:
            st.success("✅ AGORA FOI! SALVO COM SUCESSO.")
        else:
            # Esta linha vai nos dizer EXATAMENTE qual nome de coluna está errado
            st.error(f"Erro {response.status_code}: {response.text}")
