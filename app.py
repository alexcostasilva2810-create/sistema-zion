import streamlit as st
import requests

st.set_page_config(page_title="Zion Tecnologia", layout="wide")

# LIMPANDO O ERRO DE ASPAS AUTOMATICAMENTE
# Mesmo que o Segredo tenha salvo com aspas ou barras, esse código limpa tudo:
TOKEN = st.secrets["notion"]["token"].strip().replace('"', '').replace('\\', '')
DATABASE = st.secrets["notion"]["database_id"].strip().replace('"', '').replace('\\', '')

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

st.title("🚨 Agendamento Zion")

with st.form("form_final"):
    os_num = st.text_input("Nº OS")
    cliente = st.text_input("CLIENTE")
    data = st.date_input("DATA")
    
    btn = st.form_submit_button("✅ SALVAR AGORA")
    
    if btn:
        payload = {
            "parent": {"database_id": DATABASE},
            "properties": {
                "Nº OS": {"title": [{"text": {"content": os_num}}]},
                "CLIENTE": {"rich_text": [{"text": {"content": cliente}}]},
                "INÍCIO": {"rich_text": [{"text": {"content": str(data)}}]}
            }
        }
        
        # Fazendo a chamada para o Notion
        res = requests.post("https://api.notion.com/v1/pages", headers=headers, json=payload)
        
        if res.status_code == 200:
            st.success("🎉 FINALMENTE! SALVO COM SUCESSO NO NOTION.")
        else:
            # Se ainda der erro, o código vai mostrar exatamente o que o Notion recebeu
            st.error(f"Erro {res.status_code}: {res.text}")
            st.info(f"ID utilizado (limpo): {DATABASE}")
