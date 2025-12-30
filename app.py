import streamlit as st
import os

# 1. Configuração da Página
st.set_page_config(page_title="ZION TECNOLOGIA", layout="wide")

# 2. Inicialização da Lista de Empurradores
if 'lista_empurradores' not in st.session_state:
    st.session_state.lista_empurradores = ["SAMUEL PONTES", "RODRIGO SANTANA", "JOÃO DIAS"]

# 3. Barra Lateral com Logo e Menu
with st.sidebar:
    # Procura a imagem logo.png (ou Logo.png)
    if os.path.exists("logo.png"):
        st.image("logo.png", use_container_width=True)
    elif os.path.exists("Logo.png"):
        st.image("Logo.png", use_container_width=True)
    else:
        st.warning("Arquivo logo.png não detectado.")
    
    st.markdown("### MENU PRINCIPAL")
    aba = st.radio("Selecione:", ["🏠 Início", "📝 Nova O.S", "👥 Cadastrar Nomes"])

# 4. Tela de Início (Capa)
if aba == "🏠 Início":
    st.markdown("<h1 style='text-align: center;'>ZION TECNOLOGIA</h1>", unsafe_allow_html=True)
    st.divider()
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        if os.path.exists("logo.png"):
            st.image("logo.png", use_container_width=True)
        st.info("Sistema de Gestão de Vigilância")

# 5. Tela de Cadastro (O.S Bloqueada)
elif aba == "📝 Nova O.S":
    st.subheader("📝 Cadastro de Ordem de Serviço")
    with st.form("form_os"):
        c1, c2 = st.columns(2)
        with c1:
            pedido = st.text_input("PEDIDO")
            os_num = st.number_input("NÚMERO DA O.S", min_value=1, step=1)
        with c2:
            # Lista suspensa dinâmica
            empurrador = st.selectbox("EMPURRADOR", st.session_state.lista_empurradores)
            status = st.selectbox("STATUS", ["ANDAMENTO", "ENCERRADO"])
        
        # Botão de salvar
        enviar = st.form_submit_button("SALVAR REGISTRO")
        if enviar:
            st.success(f"O.S {os_num} salva e bloqueada!")

# 6. Gerenciar Nomes (Onde você cria os cadastros)
elif aba == "👥 Cadastrar Nomes":
    st.subheader("👥 Adicionar novo Empurrador")
    novo = st.text_input("Nome completo:").upper()
    if st.button("Salvar Nome"):
        if novo and novo not in st.session_state.lista_empurradores:
            st.session_state.lista_empurradores.append(novo)
            st.success("Nome adicionado à lista suspensa!")
            # O rerun deve estar sozinho em sua própria linha
            st.rerun()
