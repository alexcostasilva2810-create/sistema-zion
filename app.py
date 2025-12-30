import streamlit as st
import os

# Configuração
st.set_page_config(page_title="ZION TECNOLOGIA", layout="wide")

# Memória dos nomes
if 'empurradores' not in st.session_state:
    st.session_state.empurradores = ["SAMUEL PONTES", "RODRIGO SANTANA", "JOÃO DIAS"]

# Barra Lateral
with st.sidebar:
    # Tenta carregar a logo independente da letra ser maiúscula ou minúscula
    nome_arquivo = "logo.png"
    if os.path.exists(nome_arquivo):
        st.image(nome_arquivo, use_container_width=True)
    else:
        st.warning("⚠️ Renomeie a foto para logo.png no GitHub")
    
    st.title("ZION")
    menu = st.radio("Menu", ["🏠 Início", "📝 Nova O.S", "👥 Cadastrar Nomes"])

# --- TELA: NOVA O.S ---
if menu == "📝 Nova O.S":
    st.subheader("Cadastro de O.S")
    with st.form("form_os"):
        col1, col2 = st.columns(2)
        with col1:
            pedido = st.text_input("PEDIDO")
            # Número da O.S - Fixo após salvar
            os_num = st.number_input("NÚMERO DA O.S", min_value=1, step=1)
        with col2:
            # Lista suspensa que você controla
            empurrador = st.selectbox("EMPURRADOR", st.session_state.empurradores)
            status = st.selectbox("STATUS", ["ANDAMENTO", "ENCERRADO"])
        
        if st.form_submit_button("CONCLUIR CADASTRO"):
            st.success(f"O.S {os_num} salva!")

# --- TELA: GERENCIAR NOMES ---
elif menu == "👥 Cadastrar Nomes":
    st.subheader("Gerenciar Lista de Empurradores")
    novo = st.text_input("Novo nome:").upper()
    if st.button("Adicionar"):
        if novo and novo not in st.session_state.empurradores:
            st.session_state.empurradores.append(novo)
            st.success("Nome adicionado!")
            st.rerun()
