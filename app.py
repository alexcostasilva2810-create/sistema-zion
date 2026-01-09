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
    # Título da tela conforme sua solicitação
    st.markdown('<div class="welcome-text" style="font-size:35px; margin-top:0px;">🚀 Ordens de Serviço</div>', unsafe_allow_html=True)
    
    # CSS para garantir que todas as letras dos campos fiquem BRANCAS
    st.markdown("""
        <style>
            label { color: white !important; font-weight: bold !important; font-size: 15px !important; }
            .stMarkdown h3 { color: #0096ff !important; }
            input { color: white !important; }
        </style>
    """, unsafe_allow_html=True)

    if st.button("⬅️ VOLTAR PARA HOME"):
        st.session_state.pagina = "🏠 HOME"
        st.rerun()

    st.write("---")

    # Formulário com os 17 campos (Nº O.S. como primeiro campo)
    with st.form("form_notion_zion"):
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("### 📝 Identificação")
            # CAMPO Nº 1: AGORA É O NÚMERO DA O.S.
            f1_os = st.text_input("1. Nº O.S.") 
            f2_cliente = st.text_input("2. CLIENTE")
            f3_inicio = st.date_input("3. INÍCIO DA MISSÃO", format="DD/MM/YYYY")
            f4_tipo = st.selectbox("4. TIPO", ["ESCOLTA", "VIGILANTE"])
            f5_embarque = st.time_input("5. HORA DE EMBARQUE")
            f6_local = st.text_input("6. LOCAL")

        with col2:
            st.markdown("### 🕒 Cronograma")
            f7_empurrador = st.text_input("7. EMPURRADOR")
            f8_dt_saida = st.date_input("8. DT SAÍDA", format="DD/MM/YYYY")
            f9_fim_missao = st.date_input("9. FIM DA MISSÃO", format="DD/MM/YYYY")
            f10_status = st.selectbox("10. STATUS", ["Em Andamento", "Encerrado", "Cancelado"])
            f11_servico = st.text_input("11. SERVIÇO")
            f12_escolta1 = st.text_input("12. ESCOLTA 1")

        with col3:
            st.markdown("### 🚢 Detalhes da Operação")
            f13_escolta2 = st.text_input("13. ESCOLTA 2")
            f14_balsa = st.text_input("14. BALSA")
            f15_destino = st.text_input("15. DESTINO")
            f16_descricao = st.text_area("16. DESCRIÇÃO")
            f17_assinatura = st.text_input("17. ASSINATURA")

        st.write("---")
        
        # Botão de salvamento
        if st.form_submit_button("💾 SALVAR NA BASE DE DADOS NOTION"):
            if f1_os:
                st.success(f"✅ Ordem de Serviço Nº {f1_os} para {f2_cliente} registrada com sucesso!")
            else:
                st.warning("⚠️ Por favor, preencha o Nº da O.S.")

    # Rodapé Zion
    st.markdown('<div class="footer-zion">ZION GESTÃO DE ESCOLTA</div>', unsafe_allow_html=True)
