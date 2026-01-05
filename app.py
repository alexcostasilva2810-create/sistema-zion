import streamlit as st
import requests

# Título da página
st.set_page_config(page_title="Zion Tecnologia", layout="wide")

# 1. Busca os dados que você salvou nos Segredos (Secrets)
NOTION_TOKEN = st.secrets["notion"]["token"]
DATABASE_ID = st.secrets["notion"]["database_id"]

headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

st.title("🚨 Agendamento Zion")

# 2. Cria o formulário na tela
with st.form("form_agendamento", clear_on_submit=True):
    col1, col2 = st.columns(2)
    with col1:
        os_num = st.text_input("Nº OS")
        pedido = st.text_input("PEDIDO")
        cliente = st.text_input("CLIENTE")
        tipo = st.selectbox("TIPO", ["ESCOLTA", "VIGILÂNCIA", "OUTROS"])
    with col2:
        data_ini = st.date_input("INÍCIO", format="DD/MM/YYYY")
        hora_ini = st.text_input("HORA INÍCIO (ex: 0800)")
        data_fim = st.date_input("FIM", format="DD/MM/YYYY")
        hora_fim = st.text_input("HORA FIM (ex: 1800)")

    descricao = st.text_area("DESCRIÇÃO")
    assinatura = st.text_input("ASSINATURA")

    submit = st.form_submit_button("✅ SALVAR OPERAÇÃO")

    if submit:
        # 3. Envia os dados para o Notion
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
        
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code == 200:
            st.success("✅ SALVO COM SUCESSO NO NOTION!")
        else:
            # Se der erro, ele vai te dizer qual coluna está com nome errado
            st.error(f"Erro {response.status_code}: Verifique se os nomes das colunas na tabela são iguais aos do código.")
