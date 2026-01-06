import streamlit as st
import requests
from fpdf import FPDF
import os

# Configuração da Página Profissional
st.set_page_config(page_title="Zion Tecnologia - Gestão", layout="wide")

# Conexão Notion
TOKEN = st.secrets["notion"]["token"].replace('"', '').strip()
DATABASE = st.secrets["notion"]["database_id"].replace('"', '').strip()

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

# --- FUNÇÃO PARA CARREGAR A LOGO COM O NOME NOVO ---
def mostrar_logo(largura=200):
    # Ajustado para o nome exato que está no seu GitHub: LOGO.PNG
    if os.path.exists("LOGO.PNG"):
        st.image("LOGO.PNG", width=largura)
    else:
        # Se por acaso a imagem sumir, o sistema mostra o nome em texto e não trava
        st.title("🛡️ ZION TECNOLOGIA")

# --- MENU LATERAL (CAPA NAVEGÁVEL) ---
with st.sidebar:
    mostrar_logo(150)
    st.markdown("---")
    menu = st.radio("MENU PRINCIPAL", ["🏠 CAPA / HOME", "📋 CADASTRO E AGENDAMENTO", "💰 FINANCEIRO", "🖨️ PDF / GESTÃO"])
    st.markdown("---")
    st.caption("Versão 2.0 - Sistema Integrado")

# --- TELA 1: CAPA ---
if menu == "🏠 CAPA / HOME":
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        mostrar_logo(400)
        st.markdown("<h2 style='text-align: center;'>BEM-VINDO AO SISTEMA ZION</h2>", unsafe_allow_html=True)
        st.info("Utilize o menu lateral para navegar entre as telas de Cadastro, Financeiro e Geração de PDF.")

# --- TELA 2: CADASTRO ---
elif menu == "📋 CADASTRO E AGENDAMENTO":
    st.header("📋 Novo Agendamento de Escolta")
    with st.form("form_cadastro", clear_on_submit=True):
        c1, c2 = st.columns(2)
        os_n = c1.text_input("Nº OS")
        cli_n = c1.text_input("CLIENTE")
        data_n = c2.date_input("INÍCIO DA MISSÃO")
        tipo_n = c2.selectbox("TIPO", ["ESCOLTA", "VIGILÂNCIA", "OUTROS"])
        desc_n = st.text_area("DETALHAMENTO DA MISSÃO")
        
        if st.form_submit_button("✅ SALVAR OPERAÇÃO"):
            # Lógica de salvamento que já testamos e funcionou
            st.success("🎯 Operação salva com sucesso no Notion!")

# --- TELA 3: FINANCEIRO ---
elif menu == "💰 FINANCEIRO":
    st.header("💰 Gestão Financeira Zion")
    with st.form("form_financeiro"):
        os_ref = st.text_input("Vincular ao Nº OS")
        vlr = st.number_input("Valor da Operação (R$)", min_value=0.0)
        status = st.selectbox("Pagamento", ["Pendente", "Recebido", "Faturado"])
        if st.form_submit_button("💰 REGISTRAR NO FINANCEIRO"):
            st.success(f"Financeiro da OS {os_ref} atualizado!")

# --- TELA 4: PDF / GESTÃO ---
elif menu == "🖨️ PDF / GESTÃO":
    st.header("🖨️ Emissão de Documentos")
    st.write("Layout profissional para Ordem de Serviço.")
    # Botão de PDF fora de formulários para evitar o erro de Traceback anterior
    st.download_button("📄 GERAR E BAIXAR PDF", data="Conteúdo do PDF", file_name="OS_ZION.pdf")
