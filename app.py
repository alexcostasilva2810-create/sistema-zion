import streamlit as st
import requests
import pandas as pd
from fpdf import FPDF
from datetime import datetime
import io

# 1. CONFIGURAÇÃO DE TELA (Mobile-First)
st.set_page_config(
    page_title="Zion Tecnologia", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# 2. MOTOR DE NAVEGAÇÃO (Evita erro de NameError)
if 'pagina' not in st.session_state:
    st.session_state.pagina = "🏠 HOME"

def navegar(destino):
    st.session_state.pagina = destino
    st.rerun()

# 3. ESTILO VISUAL (Fundo Azul Royal e Letras Brancas)
st.markdown("""
    <style>
    /* Fundo do App */
    .stApp { 
        background: linear-gradient(135deg, #001a4d 0%, #003399 100%); 
    }
    
    /* Textos Globais */
    h1, h2, h3, p, span, label { color: white !important; }
    
    /* Botões Grandes para Celular */
    .stButton>button { 
        width: 100%; 
        border-radius: 12px; 
        height: 3.8em; 
        font-weight: bold; 
        background-color: white !important; 
        color: #001a4d !important;
        border: none;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.3);
        margin-bottom: 10px;
    }
    
    /* Cards de Destaque */
    .card-zion {
        background: rgba(255, 255, 255, 0.1);
        padding: 20px; 
        border-radius: 15px; 
        border: 1px solid rgba(255, 255, 255, 0.2);
        text-align: center; 
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)
# ============================================================
# # ........ BLOCO: HOME (MENU PRINCIPAL) ........ #
# ============================================================
if st.session_state.pagina == "🏠 HOME":
    # Configuração de Estilo Específica para a Home
    st.markdown("""
        <style>
        /* Fundo Azul Royal com sobreposição de Dashboard */
        .stApp {
            background: linear-gradient(rgba(0, 26, 77, 0.8), rgba(0, 51, 153, 0.8)), 
                        url('https://img.freepik.com/free-vector/abstract-digital-technology-background-with-network-connection-lines_1017-25552.jpg');
            background-size: cover;
            background-attachment: fixed;
        }
        
        /* Container dos Cards */
        .card-home {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(15px);
            border-radius: 25px;
            padding: 30px;
            border: 1px solid rgba(255, 255, 255, 0.2);
            text-align: center;
            margin-bottom: 20px;
            min-height: 320px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            transition: 0.3s;
        }
        
        .card-home:hover {
            transform: scale(1.02);
            border: 1px solid #ffdb58; /* Brilho dourado no hover */
        }

        .icon-img {
            width: 120px;
            margin-bottom: 15px;
            filter: drop-shadow(0px 10px 15px rgba(0,0,0,0.3));
        }

        h1 { font-size: 40px !important; font-weight: 800 !important; margin-bottom: 0px !important; }
        h3 { font-size: 22px !important; letter-spacing: 1px; margin-top: 10px !important; }
        </style>
    """, unsafe_allow_html=True)

    # Título Principal
    st.markdown("<h1 style='text-align: center; padding-bottom: 40px;'>ZION TECNOLOGIA</h1>", unsafe_allow_html=True)

    # Grid de Navegação
    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        st.markdown(f"""
            <div class="card-home">
                <img src="https://cdn-icons-png.flaticon.com/512/6819/6819643.png" class="icon-img">
                <h3>CADASTRO</h3>
                <p style='font-size: 14px; opacity: 0.8;'>Registro Inteligente</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("ABRIR", key="h_cad"): 
            navegar("📋 CADASTRO")

    with col2:
        st.markdown(f"""
            <div class="card-home">
                <img src="https://cdn-icons-png.flaticon.com/512/2693/2693507.png" class="icon-img">
                <h3 style='color: #FFD700 !important;'>ORDEM SERVIÇO</h3>
                <p style='font-size: 14px; opacity: 0.8;'>Agenda e Operação</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("ABRIR", key="h_grade"): 
            navegar("📊 GRADE")

    with col3:
        st.markdown(f"""
            <div class="card-home">
                <img src="https://cdn-icons-png.flaticon.com/512/10543/10543111.png" class="icon-img">
                <h3>FINANCEIRO</h3>
                <p style='font-size: 14px; opacity: 0.8;'>Calculadora e Métricas</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("ABRIR", key="h_fin"): 
            navegar("💰 FINANCEIRO")
# ============================================================
# # ........ BLOCO: CADASTRO (REGISTRO) ........ #
# ============================================================
elif st.session_state.pagina == "📋 CADASTRO":
    st.markdown("<h1>📋 NOVO LANÇAMENTO</h1>", unsafe_allow_html=True)
    if st.button("⬅️ VOLTAR PARA HOME", key="c1"): navegar("🏠 HOME")
    
    with st.form("form_registro"):
        st.markdown("### Preencha os dados da Escolta")
        os_input = st.text_input("Número da O.S")
        cliente_input = st.text_input("Cliente")
        data_input = st.date_input("Data do Serviço", datetime.now())
        valor_input = st.number_input("Valor R$", min_value=0.0)
        
        if st.form_submit_button("CONCLUIR REGISTRO"):
            # Lógica para enviar ao Notion aqui
            st.success("Dados salvos com sucesso!")

# ============================================================
# # ........ BLOCO: GRADE (ORDEM DE SERVIÇO) ........ #
# ============================================================
elif st.session_state.pagina == "📊 GRADE":
    st.markdown("<h1>📊 GRADE OPERACIONAL</h1>", unsafe_allow_html=True)
    if st.button("⬅️ VOLTAR PARA HOME", key="g1"): navegar("🏠 HOME")
    
    # Exemplo de listagem (Simulando dados do Notion)
    st.markdown("### Escoltas Agendadas")
    
    # Aqui entra o seu loop de dados: for d in dados:
    with st.container():
        c1, c2 = st.columns([4, 1])
        c1.markdown("**O.S: 2024-001** | Cliente: Transportadora X", unsafe_allow_html=True)
        if c2.button("PDF", key="p1"):
            st.toast("Gerando documento...")
        st.markdown("---")

# ============================================================
# # ........ BLOCO: FINANCEIRO (ESTRATÉGICO) ........ #
# ============================================================
elif st.session_state.pagina == "💰 FINANCEIRO":
    st.markdown("<h1>💰 PAINEL FINANCEIRO</h1>", unsafe_allow_html=True)
    if st.button("⬅️ VOLTAR PARA HOME", key="f1"): navegar("🏠 HOME")
    
    # Indicadores Rápidos (KPIs)
    col_a, col_b = st.columns(2)
    col_a.metric("Faturamento Mensal", "R$ 15.400,00")
    col_b.metric("O.S Concluídas", "24")
    
    st.markdown("### Detalhamento de Receita")
    # Exemplo de tabela para smartphone
    df_exemplo = pd.DataFrame({
        "Data": ["01/01", "02/01"],
        "Cliente": ["Loja A", "Loja B"],
        "Valor": [450.00, 1200.00]
    })
    st.dataframe(df_exemplo, use_container_width=True)
