import streamlit as st
import requests
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

# --- ESTADO DE NAVEGAÇÃO ---
if "pagina" not in st.session_state:
    st.session_state.pagina = "🏠 HOME"

# --- BARRA LATERAL ---
with st.sidebar:
    # Botão de Logo (Navegável)
    if os.path.exists("LOGO.PNG"):
        if st.button("🏠 VOLTAR À CENTRAL", use_container_width=True):
            st.session_state.pagina = "🏠 HOME"
            st.rerun()
        st.image("LOGO.PNG", use_container_width=True)
    
    st.markdown("---")
    # Menu Rádio sincronizado
    selecao = st.radio("NAVEGAÇÃO", ["🏠 HOME", "📋 AGENDAMENTO ZION", "💰 FINANCEIRO", "🖨️ GERAR PDF"],
                       index=["🏠 HOME", "📋 AGENDAMENTO ZION", "💰 FINANCEIRO", "🖨️ GERAR PDF"].index(st.session_state.pagina))
    st.session_state.pagina = selecao

# --- TELA 1: CENTRAL DE APPS ---
if st.session_state.pagina == "🏠 HOME":
    st.title("🛡️ Zion Tecnologia - Central de Gestão")
    st.write("Selecione o módulo para iniciar:")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📋 NOVO AGENDAMENTO", use_container_width=True):
            st.session_state.pagina = "📋 AGENDAMENTO ZION"
            st.rerun()
    with col2:
        if st.button("💰 FINANCEIRO", use_container_width=True):
            st.session_state.pagina = "💰 FINANCEIRO"
            st.rerun()
    with col3:
        if st.button("🖨️ GERAR PDF", use_container_width=True):
            st.session_state.pagina = "🖨️ GERAR PDF"
            st.rerun()
    
    if os.path.exists("LOGO.PNG"):
        st.image("LOGO.PNG", width=450)

# --- TELA 2: AGENDAMENTO (ESCOLTAS LADO A LADO) ---
elif st.session_state.pagina == "📋 AGENDAMENTO ZION":
    st.header("📋 Registro de Escolta")
    with st.form("form_zion", clear_on_submit=True):
        # Linha 1: Datas em formato BR
        c1, c2, c3 = st.columns(3)
        os_n = c1.text_input("Nº OS")
        data_ini = c2.date_input("DATA INÍCIO", format="DD/MM/YYYY")
        data_fim = c3.date_input("DATA FIM", format="DD/MM/YYYY")
        
        # Linha 2: Escoltas próximas
        c4, c5, c6 = st.columns(3)
        esc1 = c4.text_input("ESCOLTA 1")
        esc2 = c5.text_input("ESCOLTA 2")
        hora_emb = c6.text_input("HORA EMBARQUE")
        
        # Linha 3: Outros dados
        c7, c8, c9 = st.columns(3)
        local = c7.text_input("LOCAL")
        empurrador = c8.text_input("EMPURRADOR")
        saida = c9.text_input("SAÍDA")
        
        # Linha 4
        c10, c11, c12 = st.columns(3)
        cliente = c10.text_input("CLIENTE")
        balsa = c11.text_input("BALSA")
        destino = c12.text_input("DESTINO")
        
        pedido = st.text_input("PEDIDO")
        assinatura = st.text_input("ASSINATURA")
        desc = st.text_area("DESCRIÇÃO")

        if st.form_submit_button("✅ SALVAR OPERAÇÃO"):
            st.success("🎯 Dados registrados com sucesso!")

# --- TELAS VAZIAS (PARA NÃO DAR ERRO) ---
elif st.session_state.pagina == "💰 FINANCEIRO":
    st.header("💰 Módulo Financeiro")
elif st.session_state.pagina == "🖨️ GERAR PDF":
    st.header("🖨️ Emissão de Documentos")
