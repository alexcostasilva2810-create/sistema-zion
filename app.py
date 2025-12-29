import streamlit as st

# Configuração da Página
st.set_page_config(page_title="ZION TECNOLOGIA", layout="wide")

# Inicializa a lista de empurradores se ela não existir
if 'lista_empurradores' not in st.session_state:
    st.session_state.lista_empurradores = ["SAMUEL PONTES", "RODRIGO SANTANA", "JOÃO DIAS"]

# --- MENU LATERAL ---
with st.sidebar:
    try:
        st.image("logo.png", use_container_width=True)
    except:
        st.warning("Suba o arquivo logo.png no GitHub")
    
    st.markdown("<h2 style='text-align: center;'>SISTEMA ZION</h2>", unsafe_allow_html=True)
    escolha = st.radio("Navegação", ["🏠 Início", "📝 Nova O.S", "👥 Cadastrar Empurrador"])

# --- TELA 1: CAPA ---
if escolha == "🏠 Início":
    st.markdown("<h1 style='text-align: center;'>ZION TECNOLOGIA</h1>", unsafe_allow_html=True)
    st.divider()
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        try:
            st.image("logo.png", use_container_width=True)
        except:
            st.info("Aguardando logo.png no GitHub.")

# --- TELA 2: NOVA O.S ---
elif escolha == "📝 Nova O.S":
    st.title("📝 Cadastro de Missão")
    with st.form("form_os", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            pedido = st.text_input("PEDIDO")
            os_num = st.number_input("NÚMERO DA O.S", min_value=1, step=1)
            data_inicio = st.date_input("INÍCIO DA MISSÃO")
            local = st.text_input("LOCAL")
        with col2:
            empurrador = st.selectbox("EMPURRADOR", st.session_state.lista_empurradores)
            cmt = st.text_input("CMT")
            saida = st.text_input("SAÍDA")
            status = st.selectbox("STATUS", ["ANDAMENTO", "ENCERRADO"])

        if st.form_submit_button("SALVAR E BLOQUEAR O.S"):
            st.success(f"O.S {os_num} salva com sucesso!")

# --- TELA 3: CADASTRO DE NOMES ---
elif escolha == "👥 Cadastrar Empurrador":
    st.title("👥 Gerenciar Lista")
    novo_nome = st.text_input("Digite o novo nome:").upper()
    if st.button("Adicionar à Lista"):
        if novo_nome and novo_nome not in st.session_state.lista_empurradores:
            st.session_state.lista_empurradores.append(novo_nome)
            st.success("Nome adicionado!")
            st.rerun()
