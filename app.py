import streamlit as st
import requests

st.set_page_config(page_title="Zion Tecnologia", layout="wide")

# LIMPANDO OS DADOS AUTOMATICAMENTE
TOKEN = st.secrets["notion"]["token"].replace('"', '').replace('\\', '').strip()
DATABASE = st.secrets["notion"]["database_id"].replace('"', '').replace('\\', '').strip()

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

st.title("🚨 Agendamento Zion")

with st.form("form_final"):
    col1, col2 = st.columns(2)
    with col1:
        os = st.text_input("Nº OS")
        pedido = st.text_input("PEDIDO")
        cliente = st.text_input("CLIENTE")
    with col2:
        data = st.date_input("DATA INÍCIO")
        tipo = st.selectbox("TIPO", ["ESCOLTA", "VIGILÂNCIA", "OUTROS"])
        ass = st.text_input("ASSINATURA")

    desc = st.text_area("DESCRIÇÃO")
    
    submit = st.form_submit_button("✅ SALVAR OPERAÇÃO")

    if submit:
        payload = {
            "parent": {"database_id": DATABASE},
            "properties": {
                "Nº OS": {"title": [{"text": {"content": os}}]},
                "PEDIDO": {"rich_text": [{"text": {"content": pedido}}]},
                "CLIENTE": {"rich_text": [{"text": {"content": cliente}}]},
                "TIPO": {"select": {"name": tipo}},
                "INÍCIO": {"rich_text": [{"text": {"content": str(data)}}]},
                "DESCRIÇÃO": {"rich_text": [{"text": {"content": desc}}]},
                "ASSINATURA": {"rich_text": [{"text": {"content": ass}}]}
            }
        }
        res = requests.post("https://api.notion.com/v1/pages", headers=headers, json=payload)
        
        if res.status_code == 200:
            st.success("🎯 FINALMENTE! Dados salvos na tabela Zion.")
        else:
            st.error(f"Erro {res.status_code}: {res.text}")
