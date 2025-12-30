import streamlit as st

# Configuração da Página
st.set_page_config(page_title="ZION TECNOLOGIA", layout="wide")

# --- BANCO DE DADOS EM MEMÓRIA ---
# Isso cria a lista vazia se for a primeira vez que o app abre
if 'lista_empurradores' not in st.session_state:
    st.session_state.lista_empurradores = []

if 'tela' not in st.session_state:
    st.session_state.tela = "HOME"

def mudar_tela(nome_da_tela):
    st.session_state.tela = nome_da_tela

# --- BARRA LATERAL ---
with st.sidebar:
    try:
        st.image("LOGO.PNG", use_container_width=True)
    except:
        st.error("ERRO: O arquivo no GitHub deve ser LOGO.PNG")
    
    if st.button("🏠 MENU PRINCIPAL", use_container_width=True):
        mudar_tela("HOME")
    st.divider()

# --- TELA 1: HOME (LOGO CENTRAL) ---
if st.session_state.tela == "HOME":
    st.markdown("<h1 style='text-align: center;'>ZION TECNOLOGIA</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔵 ENTRAR NO SISTEMA", use_container_width=True):
            mudar_tela("MENU_ICONES")
        st.image("LOGO.PNG", use_container_width=True)

# --- TELA 2: MENU DE ÍCONES ---
elif st.session_state.tela == "MENU_ICONES":
    st.markdown("<h2 style='text-align: center;'>PAINEL DE GESTÃO</h2>", unsafe_allow_html=True)
    st.divider()
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("<h3 style='text-align: center;'>⏳ PROGRAMAÇÃO</h3>", unsafe_allow_html=True)
        if st.button("ABRIR AGENDA", use_container_width=True): mudar_tela("PROGRAMACAO")
    with c2:
        st.markdown("<h3 style='text-align: center;'>💰 FINANCEIRO</h3>", unsafe_allow_html=True)
        if st.button("ABRIR CAIXA", use_container_width=True): mudar_tela("FINANCEIRO")
    with c3:
        st.markdown("<h3 style='text-align: center;'>📝 CADASTRO</h3>", unsafe_allow_html=True)
        if st.button("NOVA O.S / NOMES", use_container_width=True): mudar_tela("CADASTRO")

# --- TELA 3: CADASTRO (DINÂMICO) ---
elif st.session_state.tela == "CADASTRO":
    st.title("📝 Cadastro e Gerenciamento")
    
    # Parte 1: Cadastrar Novo Empurrador
    with st.expander("➕ CADASTRAR NOVO EMPURRADOR NA LISTA"):
        novo_nome = st.text_input("Digite o nome completo do empurrador:").upper()
        if st.button("ADICIONAR NOME À LISTA"):
            if novo_nome and novo_nome not in st.session_state.lista_empurradores:
                st.session_state.lista_empurradores.append(novo_nome)
                st.success(f"{novo_nome} adicionado com sucesso!")
                st.rerun()

    st.divider()

    # Parte 2: Formulário de O.S
    st.subheader("Nova Ordem de Serviço")
    with st.form("form_os"):
        col_esq, col_dir = st.columns(2)
        with col_esq:
            st.text_input("PEDIDO")
            st.number_input("NÚMERO DA O.S", min_value=0)
            st.date_input("INÍCIO DA MISSÃO")
        with col_dir:
            # Aqui a lista suspensa puxa apenas o que você cadastrou acima
            st.selectbox("EMPURRADOR", options=st.session_state.lista_empurradores if st.session_state.lista_empurradores else ["Nenhum nome cadastrado"])
            st.text_input("LOCAL")
            st.selectbox("STATUS", ["ANDAMENTO", "ENCERRADO"])
        
        if st.form_submit_button("SALVAR REGISTRO"):
            st.success("O.S. registrada!")

# (Telas de apoio mantidas para não dar erro)
elif st.session_state.tela == "FINANCEIRO":
    st.title("💰 Financeiro")
    if st.button("Voltar"): mudar_tela("MENU_ICONES")
elif st.session_state.tela == "PROGRAMACAO":
    st.title("⏳ Programação")
    if st.button("Voltar"): mudar_tela("MENU_ICONES")
