import streamlit as st

# 1. Configuração inicial
st.set_page_config(page_title="ZION TECNOLOGIA", layout="wide")

# 2. Memória para os nomes (Empurradores)
if 'lista_empurradores' not in st.session_state:
    st.session_state.lista_empurradores = ["SAMUEL PONTES", "RODRIGO SANTANA", "JOÃO DIAS"]

# 3. Barra Lateral (Logo e Menu)
with st.sidebar:
    try:
        st.image("logo.png", use_container_width=True)
    except:
        st.error("Suba o arquivo logo.png no GitHub")
    
    st.markdown("### SISTEMA ZION")
    escolha = st.radio("Navegação", ["🏠 Início", "📝 Nova O.S", "👥 Cadastrar Empurrador"])

# 4. Tela de Início
if escolha == "🏠 Início":
    st.markdown("<h1 style='text-align: center;'>ZION TECNOLOGIA</h1>", unsafe_allow_html=True)
    st.divider()
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        try:
            st.image("logo.png", use_container_width=True)
        except:
            st.info("Aguardando logo.png")

# 5. Tela de Cadastro (Ordem do seu vídeo)
elif escolha == "📝 Nova O.S":
    st.title("📝 Nova O.S")
    with st.form("meu_formulario"):
        c1, c2 = st.columns(2)
        with c1:
            pedido = st.text_input("PEDIDO")
            os_num = st.number_input("NÚMERO DA O.S", min_value=1, step=1)
            data = st.date_input("INÍCIO DA MISSÃO")
        with c2:
            empurrador = st.selectbox("EMPURRADOR", st.session_state.lista_empurradores)
            local = st.text_input("LOCAL")
            status = st.selectbox("STATUS", ["ANDAMENTO", "ENCERRADO"])
        
        if st.form_submit_button("SALVAR REGISTRO"):
            st.success(f"O.S {os_num} salva!")

# 6. Cadastro de Nomes
elif escolha == "👥 Cadastrar Empurrador":
    st.title("👥 Gerenciar Lista")
    novo = st.text_input("Nome do novo empurrador:").upper()
    if st.button("Adicionar"):
        if novo and novo not in st.session_state.lista_empurradores:
            st.session_state.lista_empurradores.append(novo)
            st.success("Adicionado!")
            st.rerun()
