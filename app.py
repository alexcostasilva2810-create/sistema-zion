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

# --- BUSCA DE DADOS (TODAS AS COLUNAS) ---
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
                    "Nº OS": p.get("Nº OS", {}).get("title", [{}])[0].get("text", {}).get("content", ""),
                    "INÍCIO": p.get("INÍCIO DA MISSÃO", {}).get("date", {}).get("start", "") if p.get("INÍCIO DA MISSÃO") else "",
                    "FIM": p.get("FIM DA MISSÃO", {}).get("date", {}).get("start", "") if p.get("FIM DA MISSÃO") else "",
                    "CLIENTE": p.get("CLIENTE", {}).get("rich_text", [{}])[0].get("text", {}).get("content", ""),
                    "ESCOLTA 1": p.get("ESCOLTA 1", {}).get("rich_text", [{}])[0].get("text", {}).get("content", ""),
                    "ESCOLTA 2": p.get("ESCOLTA 2", {}).get("rich_text", [{}])[0].get("text", {}).get("content", ""),
                    "LOCAL": p.get("LOCAL", {}).get("rich_text", [{}])[0].get("text", {}).get("content", ""),
                    "DESTINO": p.get("DESTINO", {}).get("rich_text", [{}])[0].get("text", {}).get("content", "")
                })
            except: continue
        return pd.DataFrame(lista)
    return pd.DataFrame()

# --- MENU LATERAL ---
with st.sidebar:
    if os.path.exists("LOGO.PNG"):
        st.image("LOGO.PNG", use_container_width=True)
    st.markdown("---")
    menu = st.radio("NAVEGAÇÃO", ["🏠 HOME", "📋 AGENDAMENTO ZION", "📊 VER AGENDAMENTOS", "💰 FINANCEIRO", "🖨️ GERAR PDF"])

# --- TELA DE CADASTRO (TODOS OS CAMPOS RESTAURADOS) ---
if menu == "📋 AGENDAMENTO ZION":
    st.header("📋 Novo Registro de Missão")
    with st.form("form_zion", clear_on_submit=True):
        c1, c2, c3 = st.columns(3)
        
        # Coluna 1
        os_val = c1.text_input("Nº OS")
        ini_missao = c1.date_input("INÍCIO DA MISSÃO", format="DD/MM/YYYY")
        hora_emb = c1.text_input("HORA DE EMBARQUE")
        local = c1.text_input("LOCAL")
        empurrador = c1.text_input("EMPURRADOR")
        
        # Coluna 2
        saida = c2.text_input("SAÍDA")
        fim_missao = c2.date_input("FIM DA MISSÃO", format="DD/MM/YYYY")
        esc1 = c2.text_input("ESCOLTA 1")
        esc2 = c2.text_input("ESCOLTA 2")
        
        # Coluna 3
        cliente = c3.text_input("CLIENTE")
        balsa = c3.text_input("BALSA")
        destino = c3.text_input("DESTINO")
        pedido = c3.text_input("PEDIDO")
        assinatura = c3.text_input("ASSINATURA")

        desc = st.text_area("DESCRIÇÃO / DETALHAMENTO")

        if st.form_submit_button("✅ SALVAR NO NOTION"):
            payload = {
                "parent": {"database_id": DATABASE},
                "properties": {
                    "Nº OS": {"title": [{"text": {"content": os_val}}]},
                    "CLIENTE": {"rich_text": [{"text": {"content": cliente}}]},
                    "INÍCIO DA MISSÃO": {"date": {"start": str(ini_missao)}},
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
                st.error(f"Erro ao salvar: {res.text}")

elif menu == "📊 VER AGENDAMENTOS":
    st.header("📊 Operações Realizadas")
    df = buscar_dados()
    st.dataframe(df, use_container_width=True, hide_index=True)

elif menu == "🏠 HOME":
    st.image("LOGO.PNG", width=400)
    st.title("🛡️ Zion Tecnologia - Gestão de Escolta")
