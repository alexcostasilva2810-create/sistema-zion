import streamlit as st
import requests

# Configuração da página
st.set_page_config(page_title="Zion Tecnologia", layout="wide")

# Carrega as chaves dos Secrets do Streamlit
NOTION_TOKEN = st.secrets["notion"]["token"]
DATABASE_ID = st.secrets["notion"]["database_id"]

headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

st.title("🚨 Agendamento Zion")

with st.form("form_agendamento", clear_on_submit=True):
    col1, col2, col3, col4 = st.columns(4)
    with col1: os_num = st.text_input("Nº OS") # Ajustado para o nome na sua imagem
    with col2: pedido = st.text_input("PEDIDO")
    with col3: cliente = st.text_input("CLIENTE")
    with col4: tipo = st.selectbox("TIPO", ["ESCOLTA", "VIGILÂNCIA", "OUTROS"])

    col5, col6, col7, col8 = st.columns(4)
    with col5: data_ini = st.date_input("INÍCIO", format="DD/MM/YYYY")
    with col6: hora_ini = st.text_input("HORA INÍCIO (ex: 0827)")
    with col7: data_fim = st.date_input("FIM", format="DD/MM/YYYY")
    with col8: hora_fim = st.text_input("HORA FIM (ex: 1130)")

    descricao = st.text_area("DESCRIÇÃO")
    assinatura = st.text_input("ASSINATURA")

    submit = st.form_submit_button("✅ SALVAR OPERAÇÃO")

    if submit:
        url = "https://api.notion.com/v1/pages"
        payload = {
            "parent": {"database_id": DATABASE_ID},
            "properties": {
                "Nº OS": {"title": [{"text": {"content": os_num}}]},
                "PEDIDO": {"rich_text": [{"text": {"content": pedido}}]},
                "CLIENTE": {"rich_text": [{"text": {"content": cliente}}]},
                "TIPO": {"select": {"name": tipo}},
                "INÍCIO": {"rich_text": [{"text": {"content": f"{data_ini.strftime('%d/%m/%Y')} {hora_ini}"}}]},
                "FIM": {"rich_text": [{"text": {"content": f"{data_fim.strftime('%d/%m/%Y')} {hora_fim}"}}]},
                "DESCRIÇÃO": {"rich_text": [{"text": {"content": descricao}}]},
                "ASSINATURA": {"rich_text": [{"text": {"content": assinatura}}]}
            }
        }
        res = requests.post(url, headers=headers, json=payload)
        if res.status_code == 200:
            st.success("✅ Salvo com sucesso no Notion!")
        else:
            st.error(f"Erro {res.status_code}: Verifique se o ID da tabela nos Secrets está correto.")
