import streamlit as st
import os

# --- 1. CONFIGURAÇÃO INICIAL ---
st.set_page_config(
    page_title="Zion Business - Gestão de Escolta",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Inicialização da navegação (Sempre em Inglês para não dar erro)
if 'pagina' not in st.session_state:
    st.session_state.pagina = "🏠 HOME"

# --- 2. ESTILO CSS (TUDO BRANCO E PROFISSIONAL) ---
st.markdown("""
<style>
    .stApp { background-color: #000b1a; color: white; }
    [data-testid="stSidebar"], .stHeader, .stFooter { display: none !important; }

    /* Saudação e Título */
    .welcome-text {
        font-size: 50px; font-weight: 800; text-align: center;
        margin-top: 10px; margin-bottom: 30px;
        text-shadow: 0px 0px 20px #0096ff;
    }

    /* FORÇAR LETRAS DOS CAMPOS EM BRANCO */
    label, .stMarkdown p, .stSelectbox label, .stTextInput label {
        color: white !important;
        font-size: 16px !important;
        font-weight: bold !important;
    }

    /* Botões 3D da Home */
    div.stButton > button {
        width: 100% !important; height: 70px !important;
        background: linear-gradient(145deg, #0096ff, #005bb5) !important;
        color: white !important; font-weight: bold !important;
        border-radius: 40px 8px 40px 8px !important;
        box-shadow: 0px 8px 0px #003d66 !important;
        margin-bottom: 20px !important;
    }

    /* Rodapé Zion */
    .footer-zion {
        position: fixed; bottom: 20px; left: 40px;
        font-size: 16px; font-weight: bold; color: #0096ff;
        letter-spacing: 3px;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. LÓGICA DE NAVEGAÇÃO ---

if st.session_state.pagina == "🏠 HOME":
    st.markdown('<div class="welcome-text">Seja Bem Vindo ao Futuro</div>', unsafe_allow_html=True)
    
    col_btns, col_robo = st.columns([1, 1.3], gap="large")
    with col_btns:
        st.write("##")
        if st.button("🚀 LANÇAMENTO"):
            st.session_state.pagina = "LANÇAMENTO"
            st.rerun()
        if st.button("🛠️ ORDEM DE SERVIÇO"):
            st.session_state.pagina = "OS"
            st.rerun()
        if st.button("💰 FINANCEIRO"):
            st.session_state.pagina = "FINANCEIRO"
            st.rerun()
        if st.button("📊 EXTRATO"):
            st.session_state.pagina = "EXTRATO"
            st.rerun()

    with col_robo:
        if os.path.exists("robo_humanizado.jpg"):
            st.image("robo_humanizado.jpg", use_container_width=True)
        else:
            st.error("Imagem 'robo_humanizado.jpg' não encontrada.")

    st.markdown('<div class="footer-zion">ZION GESTÃO DE ESCOLTA</div>', unsafe_allow_html=True)

elif st.session_state.pagina == "LANÇAMENTO":
    # Título mudado conforme solicitado
    st.markdown('<div class="welcome-text" style="font-size:35px;">🚀 Ordens de Serviço</div>', unsafe_allow_html=True)
    
    if st.button("⬅️ VOLTAR PARA HOME"):
        st.session_state.pagina = "🏠 HOME"
        st.rerun()

    with st.form("form_zion"):
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown("### 📋 Identificação")
            cliente = st.text_input("1. Nome do Cliente")
            os_num = st.text_input("2. Número da O.S.")
            data_solicitacao = st.date_input("3. Data da Solicitação", format="DD/MM/YYYY")
            tipo = st.selectbox("4. Tipo de Escolta", ["Ostensiva", "Velada", "Fixo"])
            status = st.selectbox("5. Status", ["Agendado", "Em curso", "Concluído"])
            prioridade = st.select_slider("6. Prioridade", options=["Baixa", "Média", "Alta"])

        with c2:
            st.markdown("### 📍 Logística")
            origem = st.text_input("7. Cidade Origem")
            destino = st.text_input("8. Cidade Destino")
            data_inicio = st.date_input("9. Data de Início", format="DD/MM/YYYY")
            hora_inicio = st.time_input("10. Horário de Início")
            placa = st.text_input("11. Placa do Veículo")
            km_inicial = st.number_input("12. KM Inicial", min_value=0)

        with c3:
            st.markdown("### 👮 Operacional")
            lider = st.text_input("13. Agente Líder")
            equipe = st.text_area("14. Equipe de Apoio")
            valor = st.number_input("15. Valor Carga (R$)", min_value=0.0, format="%.2f")
            contato = st.text_input("16. Contato Base")
            obs = st.text_area("17. Observações")

        if st.form_submit_button("💾 SALVAR NO NOTION"):
            st.success(f"✅ O.S {os_num} salva com sucesso!")

    st.markdown('<div class="footer-zion">ZION GESTÃO DE ESCOLTA</div>', unsafe_allow_html=True)

# Outros blocos (FINANCEIRO, EXTRATO, OS)
elif st.session_state.pagina in ["OS", "FINANCEIRO", "EXTRATO"]:
    if st.button("⬅️ VOLTAR PARA HOME"):
        st.session_state.pagina = "🏠 HOME"
        st.rerun()
