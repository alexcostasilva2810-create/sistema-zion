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

# --- FUNÇÃO PARA BUSCAR DADOS (Sem travar o app) ---
def buscar_dados():
    url = f"https://api.notion.com/v1/databases/{DATABASE}/query"
    res = requests.post(url, headers=headers)
    if res.status_code == 200:
        dados = res.json()["results"]
        lista = []
        for pg in dados:
            p = pg["properties"]
            try:
                lista.append({
                    "Nº OS": p["Nº OS"]["title"][0]["text"]["content"] if p["Nº OS"]["title"] else "",
                    "DATA INÍCIO": p["DATA INÍCIO"]["date"]["start"] if p["DATA INÍCIO"]["date"] else "",
                    "CLIENTE": p["CLIENTE"]["rich_text"][0]["text"]["content"] if p["CLIENTE"]["rich_text"] else "",
                    "ESCOLTA 1": p["ESCOLTA 1"]["rich_text"][0]["text"]["content"] if p["ESCOLTA 1"]["rich_text"] else "",
                    "ESCOLTA 2": p["ESCOLTA 2"]["rich_text"][0]["text"]["content"] if p["ESCOLTA 2"]["rich_text"] else "",
                })
            except Exception:
                continue
        return pd.DataFrame(lista)
    return pd.DataFrame()

# --- BARRA LATERAL (VERSÃO QUE VOCÊ GOSTOU) ---
with st.sidebar:
    if os.path.exists("LOGO.PNG"):
        st.image("LOGO.PNG", use_container_width=True)
    st.markdown("---")
    menu = st.radio("NAVEGAÇÃO", ["🏠 HOME", "📋 AGENDAMENTO ZION", "📊 VER AGENDAMENTOS", "💰 FINANCEIRO", "🖨️ GERAR PDF"])

# --- TELA: AGENDAMENTO (TODOS OS SEUS CAMPOS MANTIDOS) ---
if menu == "📋 AGENDAMENTO ZION":
    st.header("📋 Novo Registro de Missão")
    with st.form("form_zion", clear_on_submit=True):
        c1, c2, c3 = st.columns(3)
        
        # Seus campos originais mantidos
        os_val = c1.text_input("Nº OS")
        ini_missao = c1.date_input("INICIO DA MISSÃO", format="DD/MM/YYYY")
        hora_emb = c1.text_input("HORA DE EMBARQUE")
        local = c1.text_input("LOCAL")
        empurrador = c1.text_input("EMPURRADOR")
        
        saida = c2.text_input("SAÍDA")
        fim_missao = c2.date_input("FIM DA MISSÃO", format="DD/MM/YYYY")
        esc1 = c2.text_input("ESCOLTA 1")
        esc2 = c2.text_input("ESCOLTA 2")
        
        cliente = c3.text_input("CLIENTE")
        balsa = c3.text_input("BALSA")
        destino = c3.text_input("DESTINO")
        pedido = c3.text_input("PEDIDO")
        assinatura = c3.text_input("ASSINATURA")

        desc = st.text_area("DESCRIÇÃO / DETALHAMENTO")

        if st.form_submit_button("✅ SALVAR NO NOTION"):
            # Payload corrigido para salvar de verdade
            payload = {
                "parent": {"database_id": DATABASE},
                "properties": {
                    "Nº OS": {"title": [{"text": {"content": os_val}}]},
                    "CLIENTE": {"rich_text": [{"text": {"content": cliente}}]},
                    "INICIO DA MISSÃO": {"date": {"start": str(ini_missao)}},
                    "FIM DA MISSÃO": {"date": {"start": str(fim_missao)}},
                    "ESCOLTA 1": {"rich_text": [{"text": {"content": esc1}}]},
                    "ESCOLTA 2": {"rich_text": [{"text": {"content": esc2}}]},
                    "HORA DE EMBARQUE": {"rich_text": [{"text": {"content": hora_emb}}]},
                    "LOCAL": {"rich_text": [{"text": {"content": local}}]},
                    "EMPURRADOR": {"rich_text": [{"text": {"content": empurrador}}]},
                    "SAÍDA": {"rich_text": [{"text": {"content": saida}}]},
                    "BALSA": {"rich_text": [{"text": {"content": balsa}}]},
                    "DESTINO": {"rich_text": [{"text": {"content": destino}}]},
                    "PEDIDO": {"rich_text": [{"text": {"content": pedido}}]},
                    "ASSINATURA": {"rich_text": [{"text": {"content": assinatura}}]},
                    "DESCRIÇÃO": {"rich_text": [{"text": {"content": desc}}]}
                }
            }
            res = requests.post("https://api.notion.com/v1/pages", headers=headers, json=payload)
            if res.status_code == 200:
                st.success("🎯 OPERAÇÃO SALVA COM SUCESSO!")
            else:
                st.error(f"Erro ao salvar: Verifique os nomes das colunas no Notion. {res.text}")

# --- TELA: VER AGENDAMENTOS (MANTIDA) ---
elif menu == "📊 VER AGENDAMENTOS":
    st.header("📊 Operações Realizadas")
    df = buscar_dados()
    if not df.empty:
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("Nenhum dado encontrado ou colunas incompatíveis no Notion.")

# --- TELAS DE APOIO ---
elif menu == "🏠 HOME":
    st.image("LOGO.PNG", width=400)
    st.title("Bem-vindo ao Sistema Zion")
