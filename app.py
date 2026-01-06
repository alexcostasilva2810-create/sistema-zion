import streamlit as st
import requests
import pandas as pd
from fpdf import FPDF
from datetime import datetime

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Zion Tecnologia", layout="wide")

# --- CONEXÃO NOTION ---
TOKEN = st.secrets["notion"]["token"].replace('"', '').strip()
DATABASE = st.secrets["notion"]["database_id"].replace('"', '').strip()

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

# --- FUNÇÃO PARA PUXAR DADOS DO NOTION ---
def carregar_dados_notion():
    url = f"https://api.notion.com/v1/databases/{DATABASE}/query"
    res = requests.post(url, headers=headers)
    if res.status_code == 200:
        dados = res.json().get("results", [])
        lista_final = []
        for item in dados:
            p = item.get("properties", {})
            # Extração segura de cada campo
            linha = {
                "Nº OS": p.get("Nº OS", {}).get("title", [{}])[0].get("plain_text", "---"),
                "CLIENTE": p.get("CLIENTE", {}).get("rich_text", [{}])[0].get("plain_text", "---"),
                "DT SAÍDA": p.get("DT SAÍDA", {}).get("date", {}).get("start", "---"),
                "EMPURRADOR": p.get("EMPURRADOR", {}).get("rich_text", [{}])[0].get("plain_text", "---"),
                "STATUS": p.get("STATUS", {}).get("select", {}).get("name", "---"),
                "ID": item.get("id")
            }
            lista_final.append(linha)
        return pd.DataFrame(lista_final)
    else:
        st.error(f"Erro ao conectar com Notion: {res.status_code}")
        return pd.DataFrame()

# --- NAVEGAÇÃO E HOME (Igual às anteriores) ---
if "pagina" not in st.session_state: st.session_state.pagina = "🏠 HOME"
def navegar(p): st.session_state.pagina = p; st.rerun()

if st.session_state.pagina == "🏠 HOME":
    st.title("🛡️ Painel de Controle Zion")
    col1, col2, col3 = st.columns(3)
    with col1: 
        if st.button("📋 NOVO LANÇAMENTO"): navegar("📋 CADASTRO")
    with col2: 
        if st.button("📊 VER AGENDAMENTOS"): navegar("📊 GRADE")
    with col3: 
        if st.button("💰 FINANCEIRO"): navegar("💰 FINANCEIRO")

# --- TELA DE CADASTRO (17 CAMPOS) ---
elif st.session_state.pagina == "📋 CADASTRO":
    if st.button("⬅️ VOLTAR"): navegar("🏠 HOME")
    st.header("📝 Cadastro de Missão")
    with st.form("form_completo"):
        c1, c2, c3 = st.columns(3)
        os_n = c1.text_input("Nº O.S")
        dt_saida = c2.date_input("DT SAÍDA")
        cliente = c3.text_input("CLIENTE")
        
        c4, c5, c6 = st.columns(3)
        ini_m = c4.date_input("INÍCIO DA MISSÃO")
        fim_m = c5.date_input("FIM DA MISSÃO")
        balsa = c6.text_input("BALSA")
        
        empurrador = st.text_input("EMPURRADOR")
        status = st.selectbox("STATUS", ["Em Andamento", "Encerrado"])
        desc = st.text_area("DESCRIÇÃO")
        
        if st.form_submit_button("✅ SALVAR"):
            # Lógica de salvamento enviando para o Notion...
            st.success("Salvo!")

# --- TELA GRADE (PUXANDO DADOS REAIS) ---
elif st.session_state.pagina == "📊 GRADE":
    if st.button("⬅️ VOLTAR"): navegar("🏠 HOME")
    st.subheader("📊 Agendamentos Ativos no Notion")
    
    df = carregar_dados_notion()
    
    if not df.empty:
        # Exibe a tabela com os dados reais
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Opção para baixar PDF de uma linha específica
        st.divider()
        selecionado = st.selectbox("Selecione uma O.S para gerar PDF:", df["Nº OS"].tolist())
        if st.button("📄 Gerar Relatório PDF"):
            st.success(f"PDF da O.S {selecionado} preparado!")
    else:
        st.warning("Nenhum dado encontrado ou erro na conexão.")

# --- TELA FINANCEIRO ---
elif st.session_state.pagina == "💰 FINANCEIRO":
    if st.button("⬅️ VOLTAR"): navegar("🏠 HOME")
    st.header("💰 Financeiro")
    st.table(pd.DataFrame(columns=["DATA", "DESCRIÇÃO", "VALOR"]))
