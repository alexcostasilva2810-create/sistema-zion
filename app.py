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

# --- 3. LÓGICA DA TELA HOME (COM IMAGEM CENTRALIZADA) ---
if st.session_state.pagina == "🏠 HOME":
    
    # Saudação no topo
    st.markdown('<div class="welcome-text">Seja Bem Vindo ao Futuro</div>', unsafe_allow_html=True)

    # Ajustei as colunas para [1, 1] para que fiquem com o mesmo peso e centralizadas
    # A coluna "col_espaco" serve para empurrar o conteúdo para o centro da tela
    col_vazia_lateral, col_btns, col_robo, col_vazia_lateral2 = st.columns([0.3, 1, 1.2, 0.3], gap="large")

    with col_btns:
        # Espaçador para alinhar os botões verticalmente com o centro da imagem do robô
        st.markdown('<div style="margin-top: 50px;"></div>', unsafe_allow_html=True)
        
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
        # Exibe a imagem que você salvou na pasta
        caminho_imagem = "robo_humanizado.jpg"
        if os.path.exists(caminho_imagem):
            st.image(caminho_imagem, use_container_width=True)
        else:
            st.error("⚠️ Imagem 'robo_humanizado.jpg' não encontrada na pasta.")

    # Rodapé fixo ZION
    st.markdown('<div class="footer-zion">ZION GESTÃO DE ESCOLTA</div>', unsafe_allow_html=True)

# Lógica básica para voltar das outras telas
elif rua.estado_da_sessão.página == "LANÇAMENTO":
    # Título estilizado
    rua.markdown('<div class="welcome-text" style="font-size:38px; margin-top:0px;">🚀 Painel de Lançamento</div>', unsafe_allow_html=Verdadeiro)
    
    # Botão Voltar
    se rua.botão("⬅️ VOLTAR PARA CASA"):
        rua.estado_da_sessão.página = "🏠 CASA"
        rua.reprise()

    rua.escrever("---")

    # Formulário com as 17 colunas para o Notion
    com rua.formulário("form_lancamento"):
        col1, col2, col3 = rua.colunas(3)

        com col1:
            rua.subcabeçalho("📋 Identificação")
            c1 = rua.entrada_de_texto("1. Nome do Cliente")
            c2 = rua.entrada_de_texto("2. Número da O.S.")
            c3 = rua.entrada_de_data("3. Data da Solicitação", formato="DD/MM/YYYY")
            c4 = rua.caixa_de_seleção("4. Tipo de Escolta", ["Velado", "Ostensivo", "Fixo"])
            c5 = rua.caixa_de_seleção("5. Status", ["Agendado", "Em Andamento", "Finalizado"])
            c6 = rua.seletor_deslizante("6. Prioridade", opções=["Baixa", "Média", "Alta", "Urgente"])

        com col2:
            rua.subcabeçalho("📍 Rota e Logística")
            c7 = rua.entrada_de_texto("7. Cidade Origem")
            c8 = rua.entrada_de_texto("8. Cidade Destino")
            c9 = rua.entrada_de_data("9. Previsão de Início", formato="DD/MM/YYYY")
            c10 = rua.entrada_de_hora("10. Horário de Início")
            c11 = rua.entrada_de_texto("11. Placa do Veículo")
            c12 = rua.entrada_de_número("12. KM Inicial", valor_mínimo=0)

        com col3:
            rua.subcabeçalho("👮 Operacional")
            c13 = rua.entrada_de_texto("13. Agente Líder")
            c14 = rua.área_de_texto("14. Equipe de Apoio")
            c15 = rua.entrada_de_número("15. Valor da Carga (R$)", valor_mínimo=0.0, formato="%.2f")
            c16 = rua.entrada_de_texto("16. Contato na Base")
            c17 = rua.área_de_texto("17. Observações Gerais")

        rua.escrever("---")
        
        # Botão de salvar
        se rua.botão_de_envio_do_formulário("💾 SALVAR NO NOTION"):
            rua.sucesso(f"✅ Dados da O.S {c2} registrados com sucesso!")

    # Rodapé Zion
    rua.markdown('<div class="footer-zion">ZION GESTÃO DE ESCOLTA</div>', unsafe_allow_html=Verdadeiro)
