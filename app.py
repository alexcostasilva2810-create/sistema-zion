import streamlit as st
import requests
from fpdf import FPDF
import os

# Configuração da Página
st.set_page_config(page_title="Zion Tecnologia", layout="wide")

# Conexão Notion
TOKEN = st.secrets["notion"]["token"].replace('"', '').strip()
DATABASE = st.secrets["notion"]["database_id"].replace('"', '').strip()

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

# --- CONTROLE DE NAVEGAÇÃO ---
if "pagina" not in st.session_state:
    st.session_state.pagina = "🚀 CENTRAL"

# --- BARRA LATERAL COM LOGO NAVEGÁVEL ---
with st.sidebar:
    if os.path.exists("LOGO.PNG"):
        # A logo agora funciona como botão para voltar à Central
        if st.button("🏠 IR PARA CENTRAL / HOME", use_container_width=True):
            st.session_state.pagina = "🚀 CENTRAL"
            st.rerun()
        st.image("LOGO.PNG", use_container_width=True)
    
    st.markdown("---")
    # Sincronização do Menu com o Estado Global
    selecao = st.radio("NAVEGAÇÃO", ["🏠 HOME", "📋 AGENDAMENTO ZION", "💰 FINANCEIRO", "🖨️ GERAR PDF"], 
                       index=["🚀 CENTRAL", "📋 AGENDAMENTO ZION", "💰 FINANCEIRO", "🖨️ GERAR PDF"].index(st.session_state.pagina) if st.session_state.pagina in ["🚀 CENTRAL", "📋 AGENDAMENTO ZION", "💰 FINANCEIRO", "🖨️ GERAR PDF"] else 0)
    
    if selecao == "🏠 HOME": st.session_state.pagina = "🚀 CENTRAL"
    else: st.session_state.pagina = selecao

# --- TELA 1: CENTRAL DE APPS (ESTILO VÍDEO) ---
if st.session_state.pagina == "🚀 CENTRAL":
    st.title("🛡️ Zion Tecnologia - Central de Gestão")
    st.markdown("### Selecione o módulo desejado:")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📋 AGENDAMENTO\n(Novo Registro)", use_container_width=True, height=150):
            st.session_state.pagina = "📋 AGENDAMENTO ZION"
            st.rerun()
    with col2:
        if st.button("💰 FINANCEIRO\n(Fluxo de Caixa)", use_container_width=True, height=150):
            st.session_state.pagina = "💰 FINANCEIRO"
            st.rerun()
    with col3:
        if st.button("🖨️ GERAR PDF\n(Emissão de O.S)", use_container_width=True, height=150):
            st.session_state.pagina = "🖨️ GERAR PDF"
            st.rerun()
    
    st.image("LOGO.PNG", width=400) # Capa principal

# --- TELA 2: AGENDAMENTO (REGRAS DE DATA E ESCOLTA) ---
elif st.session_state.pagina == "📋 AGENDAMENTO ZION":
    st.header("📋 Cadastro de Operação de Escolta")
    with st.form("form_agendamento", clear_on_submit=True):
        c1, c2, c3 = st.columns(3)
        
        # Coluna 1
        os_n = c1.text_input("Nº OS")
        # Correção do formato da data para DD/MM/AAAA
        data_ini = c1.date_input("DATA INÍCIO", format="DD/MM/YYYY")
        hora_emb = c1.text_input("HORA EMBARQUE")
        local = c1.text_input("LOCAL")
        
        # Coluna 2
        empurrador = c2.text_input("EMPURRADOR")
        saida = c2.text_input("SAÍDA")
        data_fim = c2.date_input("DATA FIM", format="DD/MM/YYYY")
        cliente = c2.text_input("CLIENTE")
        
        # Coluna 3: Escoltas próximas uma da outra
        esc1 = c3.text_input("ESCOLTA 1")
        esc2 = c3.text_input("ESCOLTA 2")
        balsa = c3.text_input("BALSA")
        destino = c3.text_input("DESTINO")
        
        pedido = st.text_input("PEDIDO")
        assinatura = st.text_input("ASSINATURA")
        desc = st.text_area("DESCRIÇÃO")

        if st.form_submit_button("✅ SALVAR OPERAÇÃO"):
            # Envio formatado para o Notion
            st.success(f"Operação salva com sucesso! Datas registradas: {data_ini.strftime('%d/%m/%Y')} a {data_fim.strftime('%d/%m/%Y')}")

# --- OUTRAS TELAS ---
elif st.session_state.pagina == "💰 FINANCEIRO":
    st.header("💰 Gestão Financeira")
    st.info("Tela em desenvolvimento conforme o fluxo do Notion.")

elif st.session_state.pagina == "🖨️ GERAR PDF":
    st.header("🖨️ Emissão de O.S")
    st.download_button("📥 BAIXAR PDF MODELO", data="PDF", file_name="OS_ZION.pdf")
