import streamlit as st
import requests

st.set_page_config(page_title="Zion Tecnologia", layout="wide")

# LIMPANDO OS DADOS AUTOMATICAMENTE
# O código abaixo remove aspas extras que podem estar travando o sistema
TOKEN = st.secrets["notion"]["token"].replace('"', '').replace('\\', '').strip()
DATABASE = st.secrets["notion"]["database_id"].replace('"', '').replace('\\', '').strip()

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

st.title("🚨 Agendamento Zion")

with st.form("meu_form"):
    os = st.text_input("Nº OS")
    cliente = st.text_input("CLIENTE")
    data = st.date_input("DATA")
    
    btn = st.form_submit_button("✅ SALVAR AGORA")
    
    if btn:
        payload = {
            "parent": {"database_id": DATABASE},
            "properties": {
                "Nº OS": {"title": [{"text": {"content": os}}]},
                "CLIENTE": {"rich_text": [{"text": {"content": cliente}}]},
                "INÍCIO": {"rich_text": [{"text": {"content": str(data)}}]}
            }
        }
        res = requests.post("https://api.notion.com/v1/pages", headers=headers, json=payload)
        
        if res.status_code == 200:
            st.success("CONSEGUIMOS! SALVO NO NOTION.")
        else:
            st.error(f"Erro {res.status_code}: {res.text}")
