import streamlit as st

# Configuração da página
st.set_page_config(page_title="ZION TECNOLOGIA", layout="wide")

# Memória para os nomes dos empurradores
if 'lista' not in st.session_state:
    st.session_state.lista = ["SAMUEL PONTES", "RODRIGO SANTANA", "JOÃO DIAS"]

# --- MENU LATERAL ---
with st.sidebar:
    # A logo aqui funciona como o botão de início
    if st.button("🏠 IR PARA O INÍCIO", use_container_width=True):
        st.session_state.aba = "Início"
    
    st.image("logo.png", use_container_width=True)
    st.markdown("---")
    
    # Navegação simples
    if 'aba' not in st.session_state:
        st.session_state.aba = "Início"
        
    menu = st.radio("Selecione:", ["Início", "Nova O.S", "Cadastrar Nomes"])
    st.session_state.aba = menu

# --- TELA 1: INÍCIO ---
if st.session_state.aba == "Início":
    st.markdown("<h1 style='text-align: center;'>ZION TECNOLOGIA</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.image("logo.png")

# --- TELA 2: FORMULÁRIO (ORDEM DO SEU VÍDEO) ---
elif st.session_state.aba == "Nova O.S":
    st.title("📝 Nova O.S")
    with st.form("form_os"):
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("PEDIDO")
            st.number_input("NÚMERO DA O.S", min_value=0, step=1)
            st.date_input("INÍCIO DA MISSÃO")
            st.text_input("HORA DO EMBARQUE")
            st.text_input("LOCAL")
        with col2:
            st.selectbox("EMPURRADOR", st.session_state.lista)
            st.text_input("CMT")
            st.text_input("SAÍDA")
            st.date_input("FIM DA MISSÃO")
            st.text_input("HORA/TÉRMINO DA MISSÃO")
        
        if st.form_submit_button("CONCLUIR CADASTRO"):
            st.success("O.S Salva e Bloqueada!")

# --- TELA 3: CADASTRAR NOMES ---
elif st.session_state.aba == "Cadastrar Nomes":
    st.title("👥 Gerenciar Nomes")
    novo = st.text_input("Nome do Empurrador:").upper()
    if st.button("Adicionar"):
        if novo and novo not in st.session_state.lista:
            st.session_state.lista.append(novo)
            st.success("Nome adicionado!")
            st.rerun()
