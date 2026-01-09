import streamlit as st
import os

# --- 1. CONFIGURAÇÃO INICIAL ---
st.set_page_config(
    page_title="Zion Business - Gestão de Escolta",
    layout="wide",
    initial_sidebar_state="collapsed"
)

if 'pagina' not in st.session_state:
    st.session_state.pagina = "🏠 HOME"

# --- 2. ESTILO CSS (DESIGN 3D E RODAPÉ) ---
st.markdown("""
<style>
    .stApp { background-color: #000b1a; color: white; }
    [data-testid="stSidebar"], .stHeader, .stFooter { display: none !important; }

    /* Saudação */
    .welcome-text {
        font-size: 55px; font-weight: 800; text-align: center;
        margin-top: 20px; margin-bottom: 40px;
        text-shadow: 0px 0px 20px #0096ff;
    }

    /* BOTÕES 3D - ESTILO MÃO DE ROBÔ */
    div.stButton > button {
        width: 100% !important; height: 75px !important;
        background: linear-gradient(145deg, #0096ff, #005bb5) !important;
        color: white !important; font-size: 19px !important;
        font-weight: bold !important; text-transform: uppercase;
        border: none !important;
        border-radius: 40px 8px 40px 8px !important; /* Formato Mão de Robô */
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
        position: fixed; bottom: 20px; left: 40px;
        font-size: 16px; font-weight: bold; color: #0096ff;
        letter-spacing: 3px; text-transform: uppercase;
    }

    [data-testid="stImage"] img {
        border-radius: 20px;
        filter: drop-shadow(0px 0px 35px rgba(0, 150, 255, 0.3));
    }
</style>
""", unsafe_allow_html=True)

# --- 3. LÓGICA DA TELA HOME ---
if st.session_state.pagina == "🏠 HOME":
    st.markdown('<div class="welcome-text">Seja Bem Vindo ao Futuro</div>', unsafe_allow_html=True)

    col_btns, col_robo = st.columns([1, 1.3], gap="large")

    with col_btns:
        st.write("##") 
        if st.button("🚀 LANÇAMENTO"):
            st.session_state.pagina = "LANÇAMENTO"; st.rerun()
        if st.button("🛠️ ORDEM DE SERVIÇO"):
            st.session_state.pagina = "OS"; st.rerun()
        if st.button("💰 FINANCEIRO"):
            st.session_state.pagina = "FINANCEIRO"; st.rerun()
        if st.button("📊 EXTRATO"):
            st.session_state.pagina = "EXTRATO"; st.rerun()

    with col_robo:
        # TENTA CARREGAR A IMAGEM QUE VOCÊ SALVOU NA PASTA
        if os.path.exists("robo_humanizado.jpg"):
            st.image("robo_humanizado.jpg", use_container_width=True)
        else:
            st.warning("⚠️ Por favor, salve a imagem do robô como 'robo_humanizado.jpg' na mesma pasta deste código.")

    st.markdown('<div class="footer-zion">ZION GESTÃO DE ESCOLTA</div>', unsafe_allow_html=True)

# Lógica básica para voltar das outras telas
elif st.session_state.pagina in ["LANÇAMENTO", "OS", "FINANCEIRO", "EXTRATO"]:
    st.title(f"Tela: {st.session_state.pagina}")
    if st.button("⬅️ VOLTAR PARA HOME"):
        st.session_state.pagina = "🏠 HOME"; st.rerun()
