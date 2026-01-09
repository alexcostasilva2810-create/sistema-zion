import streamlit as st
import os

# --- 1. CONFIGURAÇÃO INICIAL (O TOPO DO ARQUIVO) ---
st.set_page_config(
    page_title="Zion Business - Gestão de Escolta",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Inicialização da navegação
if 'pagina' not in st.session_state:
    st.session_state.pagina = "🏠 HOME"

# --- 2. ESTILO CSS (DESIGN 3D E ROBÓTICO REAL) ---
st.markdown("""
<style>
    .stApp {
        background-color: #000b1a;
        color: white;
    }
    [data-testid="stSidebar"], .stHeader, .stFooter { display: none !important; }

    /* Saudação Centralizada */
    .welcome-text {
        font-size: 55px;
        font-weight: 800;
        text-align: center;
        margin-top: 20px;
        margin-bottom: 40px;
        text-shadow: 0px 0px 20px #0096ff;
    }

    /* BOTÕES 3D - FORMATO MÃO DE ROBÔ */
    div.stButton > button {
        width: 100% !important;
        height: 75px !important;
        background: linear-gradient(145deg, #0096ff, #005bb5) !important;
        color: white !important;
        font-size: 19px !important;
        font-weight: bold !important;
        text-transform: uppercase;
        border: none !important;
        border-radius: 40px 8px 40px 8px !important;
        box-shadow: 0px 8px 0px #003d66, 0px 15px 25px rgba(0,0,0,0.5) !important;
        transition: all 0.1s ease !important;
        margin-bottom: 25px !important;
    }

    div.stButton > button:active {
        box-shadow: 0px 2px 0px #003d66 !important;
        transform: translateY(6px) !important;
    }

    /* Rodapé ZION GESTÃO DE ESCOLTA */
    .footer-zion {
        position: fixed;
        bottom: 20px;
        left: 40px;
        font-size: 16px;
        font-weight: bold;
        color: #0096ff;
        letter-spacing: 3px;
        text-transform: uppercase;
    }

    /* Efeito na Imagem do Robô */
    [data-testid="stImage"] img {
        border-radius: 20px;
        filter: drop-shadow(0px 0px 35px rgba(0, 150, 255, 0.3));
    }
</style>
""", unsafe_allow_html=True)

# --- 3. LÓGICA DE TELAS ---

if st.session_state.pagina == "🏠 HOME":
    
    st.markdown('<div class="welcome-text">Seja Bem Vindo ao Futuro</div>', unsafe_allow_html=True)

    col_btns, col_robo = st.columns([1, 1.3], gap="large")

    with col_btns:
        st.write("##") 
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
        # TENTA CARREGAR A IMAGEM LOCAL PARA NÃO VIR UNICÓRNIO
        if os.path.exists("robo_zion.jpg"):
            st.image("robo_zion.jpg", use_container_width=True)
        else:
            # Fallback seguro com o robô humanizado direto da web caso o arquivo local não exista
            st.image("https://img.freepik.com/premium-photo/humanoid-robot-head-with-human-features-futuristic-technology-concept-generative-ai_124507-44026.jpg", use_container_width=True)

    st.markdown('<div class="footer-zion">ZION GESTÃO DE ESCOLTA</div>', unsafe_allow_html=True)

# --- OUTRAS PÁGINAS ---
elif st.session_state.pagina == "LANÇAMENTO":
    st.title("🚀 Tela de Lançamento")
    if st.button("⬅️ VOLTAR"):
        st.session_state.pagina = "🏠 HOME"
        st.rerun()
# (Repetir para os outros elifs conforme necessário...)
