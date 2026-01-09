import streamlit as st

# --- 1. CONFIGURAÇÃO INICIAL DA PÁGINA ---
st.set_page_config(
    page_title="Zion Gestão de Escolta",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Inicializa o controle de navegação
if 'pagina' not in st.session_state:
    st.session_state.pagina = "🏠 HOME"

# --- 2. ESTILO CSS (O CORAÇÃO DO DESIGN) ---
st.markdown("""
<style>
    /* Fundo Escuro Profissional */
    .stApp {
        background: #000b1a;
        color: white;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    /* Esconde elementos padrão do Streamlit para limpeza total */
    [data-testid="stSidebar"], .stHeader, .stFooter { display: none !important; }

    /* Estilização da Saudação no Topo */
    .welcome-text {
        font-size: 50px;
        font-weight: 800;
        text-align: center;
        margin-top: 30px;
        margin-bottom: 40px;
        color: #ffffff;
        text-shadow: 0px 0px 20px rgba(0, 150, 255, 0.7);
        letter-spacing: 2px;
    }

    /* BOTÕES 3D ESTILO "MÃO DE ROBÔ" */
    .stButton > button {
        width: 100% !important;
        height: 70px !important;
        background: linear-gradient(145deg, #0096ff, #005bb5) !important;
        color: white !important;
        font-size: 18px !important;
        font-weight: bold !important;
        text-transform: uppercase;
        border: none !important;
        /* Bordas Assimétricas Futuristas */
        border-radius: 45px 10px 45px 10px !important;
        /* Sombras para Efeito 3D */
        box-shadow: 0px 8px 0px #003d66, 0px 15px 25px rgba(0,0,0,0.5) !important;
        transition: all 0.1s ease !important;
        margin-bottom: 20px !important;
        cursor: pointer;
    }

    /* Efeito de Pressão ao Clicar (Afundar) */
    .stButton > button:active {
        box-shadow: 0px 2px 0px #003d66 !important;
        transform: translateY(6px) !important;
    }

    .stButton > button:hover {
        filter: brightness(1.2) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
    }

    /* Rodapé Zion Gestão de Escolta */
    .footer-zion {
        position: fixed;
        bottom: 20px;
        left: 30px;
        font-size: 15px;
        font-weight: bold;
        color: #0096ff;
        letter-spacing: 3px;
        text-transform: uppercase;
        opacity: 0.8;
    }

    /* Efeito de brilho na imagem do robô */
    [data-testid="stImage"] {
        filter: drop-shadow(0px 0px 30px rgba(0, 150, 255, 0.3));
        transition: transform 0.5s ease;
    }
    [data-testid="stImage"]:hover {
        transform: scale(1.01);
    }
</style>
""", unsafe_allow_html=True)

# --- 3. LÓGICA DE NAVEGAÇÃO ENTRE TELAS ---

# --- TELA HOME (PRINCIPAL) ---
if st.session_state.pagina == "🏠 HOME":
    
    # Saudação
    st.markdown('<div class="welcome-text">Seja Bem Vindo ao Futuro</div>', unsafe_allow_html=True)

    # Layout de Colunas: Botões à Esquerda, Robô à Direita
    col_vazia_esq, col_btns, col_robo, col_vazia_dir = st.columns([0.2, 1, 1.3, 0.2], gap="large")

    with col_btns:
        st.write("##") # Espaçador para alinhar com o centro da imagem
        
        if st.button("🚀 LANÇAMENTO"):
            st.session_state.pagina = "LANÇAMENTO"
            st.rerun()
            
        if st.button("🛠️ ORDEM DE SERVIÇO"):
            st.session_state.pagina = "ORDEM DE SERVIÇO"
            st.rerun()
            
        if st.button("💰 FINANCEIRO"):
            st.session_state.pagina = "FINANCEIRO"
            st.rerun()
            
        if st.button("📊 EXTRATO"):
            st.session_state.pagina = "EXTRATO"
            st.rerun()

    with col_robo:
        st.image("https://img.freepik.com/premium-photo/humanoid-robot-head-with-human-features-futuristic-technology-concept-generative-ai_124507-44026.jpg", use_container_width=True)

    # Rodapé fixo no canto inferior
    st.markdown('<div class="footer-zion">ZION GESTÃO DE ESCOLTA</div>', unsafe_allow_html=True)

# --- TELA DE LANÇAMENTO ---
elif st.session_state.pagina == "LANÇAMENTO":
    st.title("🚀 Novo Lançamento")
    st.write("Área para inserção de dados de escolta.")
    if st.button("⬅️ VOLTAR PARA HOME"):
        st.session_state.pagina = "🏠 HOME"
        st.rerun()

# --- TELA DE ORDEM DE SERVIÇO ---
elif st.session_state.pagina == "ORDEM DE SERVIÇO":
    st.title("🛠️ Ordens de Serviço")
    st.write("Gerenciamento de chamados e serviços.")
    if st.button("⬅️ VOLTAR PARA HOME"):
        st.session_state.pagina = "🏠 HOME"
        st.rerun()

# --- TELA DE FINANCEIRO ---
elif st.session_state.pagina == "FINANCEIRO":
    st.title("💰 Financeiro")
    st.write("Controle de contas e pagamentos.")
    if st.button("⬅️ VOLTAR PARA HOME"):
        st.session_state.pagina = "🏠 HOME"
        st.rerun()

# --- TELA DE EXTRATO ---
elif st.session_state.pagina == "EXTRATO":
    st.title("📊 Extrato Geral")
    st.write("Visualização de relatórios e movimentações.")
    if st.button("⬅️ VOLTAR PARA HOME"):
        st.session_state.pagina = "🏠 HOME"
        st.rerun()
