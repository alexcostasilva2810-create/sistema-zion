import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# Configurações iniciais
st.set_page_config(page_title="Zion Tecnologia", layout="wide")

# Conexão Notion
TOKEN = st.secrets["notion"]["token"].replace('"', '').strip()
DATABASE = st.secrets["notion"]["database_id"].replace('"', '').strip()

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

# --- FUNÇÕES DE APOIO ---
def buscar_dados():
    url = f"https://api.notion.com/v1/databases/{DATABASE}/query"
    res = requests.post(url, headers=headers)
    if res.status_code == 200:
        dados = res.json()["results"]
        lista = []
        for pg in dados:
            p = pg["properties"]
            try:
                # Cálculo financeiro baseado no tipo de serviço (Escolta ou Vigilância)
                tipo = p.get("SERVIÇO", {}).get("select", {}).get("name", "Escolta")
                valor = 1870.0 if tipo == "Escolta" else 970.0
                
                lista.append({
                    "ID": pg["id"],
                    "Nº OS": p.get("Nº OS", {}).get("title", [{}])[0].get("text", {}).get("content", ""),
                    "CLIENTE": p.get("CLIENTE", {}).get("rich_text", [{}])[0].get("text", {}).get("content", ""),
                    "INÍCIO": p.get("INÍCIO DA MISSÃO", {}).get("date", {}).get("start", ""),
                    "STATUS": p.get("STATUS", {}).get("select", {}).get("name", "Em Andamento"),
                    "VALOR": valor
                })
            except: continue
        return pd.DataFrame(lista)
    return pd.DataFrame()

# --- NAVEGAÇÃO ---
if "pagina" not in st.session_state:
    st.session_state.pagina = "🏠 HOME"

def mudar_pagina(nome):
    st.session_state.pagina = nome
    st.rerun()

# --- INTERFACE ---
with st.sidebar:
    st.image("LOGO.PNG", use_container_width=True)
    if st.button("🏠 VOLTAR AO INÍCIO", use_container_width=True):
        mudar_pagina("🏠 HOME")
    st.markdown("---")
    menu = ["🏠 HOME", "📋 AGENDAMENTO ZION", "📊 VER AGENDAMENTOS", "💰 FINANCEIRO"]
    escolha = st.radio("NAVEGAÇÃO", menu)
    st.session_state.pagina = escolha

# --- TELA 1: HOME (ÍCONE CLICÁVEL) ---
if st.session_state.pagina == "🏠 HOME":
    st.title("🛡️ Zion Tecnologia - Central de Gestão")
    st.write("Clique no ícone abaixo para acessar os módulos")
    if st.button("🔵 ACESSAR SISTEMA ZION", use_container_width=True):
        mudar_pagina("📋 AGENDAMENTO ZION")
    st.image("LOGO.PNG", width=500)

# --- TELA 2: AGENDAMENTO (LINHA ÚNICA) ---
elif st.session_state.pagina == "📋 AGENDAMENTO ZION":
    st.header("📋 Novo Registro de Missão")
    if st.button("⬅️ VOLTAR"): mudar_pagina("🏠 HOME")
    
    with st.form("form_unico", clear_on_submit=True):
        c1, c2, c3 = st.columns(3)
        os_v = c1.text_input("Nº OS")
        servico = c1.selectbox("TIPO DE SERVIÇO", ["Escolta", "Vigilância"])
        dt_ini = c1.date_input("INÍCIO DA MISSÃO")
        
        cli = c2.text_input("CLIENTE")
        esc1 = c2.text_input("ESCOLTA 1")
        esc2 = c2.text_input("ESCOLTA 2")
        
        status = c3.selectbox("STATUS INICIAL", ["Em Andamento", "Encerrado"])
        balsa = c3.text_input("BALSA")
        destino = c3.text_input("DESTINO")

        if st.form_submit_button("✅ SALVAR EM LINHA ÚNICA"):
            payload = {
                "parent": {"database_id": DATABASE},
                "properties": {
                    "Nº OS": {"title": [{"text": {"content": os_v}}]},
                    "CLIENTE": {"rich_text": [{"text": {"content": cli}}]},
                    "SERVIÇO": {"select": {"name": servico}},
                    "STATUS": {"select": {"name": status}},
                    "INÍCIO DA MISSÃO": {"date": {"start": str(dt_ini)}},
                    "ESCOLTA 1": {"rich_text": [{"text": {"content": esc1}}]},
                    "ESCOLTA 2": {"rich_text": [{"text": {"content": esc2}}]},
                    "BALSA": {"rich_text": [{"text": {"content": balsa}}]},
                    "DESTINO": {"rich_text": [{"text": {"content": destino}}]}
                }
            }
            res = requests.post("https://api.notion.com/v1/pages", headers=headers, json=payload)
            if res.status_code == 200:
                st.success("🎯 Salvo! Redirecionando...")
                mudar_pagina("📊 VER AGENDAMENTOS") # Remessa automática após salvar
            else:
                st.error(f"Erro: {res.text}")

# --- TELA 3: VER AGENDAMENTOS (TABELA COM EDIÇÃO E PDF) ---
elif st.session_state.pagina == "📊 VER AGENDAMENTOS":
    st.header("📊 Gestão de Operações")
    if st.button("⬅️ VOLTAR"): mudar_pagina("🏠 HOME")
    
    df = buscar_dados()
    if not df.empty:
        # Exibição da Tabela igual ao vídeo
        for index, row in df.iterrows():
            col_os, col_cli, col_status, col_btn = st.columns([1, 2, 1, 2])
            col_os.write(row["Nº OS"])
            col_cli.write(row["CLIENTE"])
            col_status.write(row["STATUS"])
            with col_btn:
                if st.button(f"📄 PDF/EDITAR {row['Nº OS']}", key=row["ID"]):
                    st.info(f"Gerando relatório para O.S {row['Nº OS']}...")
        st.divider()
        st.dataframe(df.drop(columns=["ID"]), use_container_width=True)
    else:
        st.warning("Nenhum dado encontrado.")

# --- TELA 4: FINANCEIRO ---
elif st.session_state.pagina == "💰 FINANCEIRO":
    st.header("💰 Controle Financeiro por Pedido")
    if st.button("⬅️ VOLTAR"): mudar_pagina("🏠 HOME")
    
    df = buscar_dados()
    if not df.empty:
        df["TOTAL"] = df["VALOR"]
        st.table(df[["Nº OS", "CLIENTE", "STATUS", "VALOR"]])
        st.metric("VALOR TOTAL GERAL", f"R$ {df['VALOR'].sum():,.2f}")
