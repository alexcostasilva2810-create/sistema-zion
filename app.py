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
import streamlit as st

# O erro anterior ocorria porque o CSS não estava dentro de uma variável string.
# Aqui definimos o bloco completo como uma constante.

MENU_HTML = """
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">

<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');

    .main-container {
        font-family: 'Poppins', sans-serif;
        display: flex;
        flex-direction: column;
        align-items: center;
        padding: 40px 10px;
    }

    /* Logo do Zion */
    .logo-zion {
        width: 200px;
        margin-bottom: 50px;
        filter: drop-shadow(0px 4px 10px rgba(0,0,0,0.1));
    }

    /* Grid de Navegação */
    .nav-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 25px;
        width: 100%;
        max-width: 500px;
    }

    /* Item de Menu (Card) */
    .menu-item {
        background: white;
        border-radius: 20px;
        padding: 30px;
        text-align: center;
        text-decoration: none;
        color: #2c3e50;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05);
        border: 1px solid #f0f0f0;
        transition: all 0.3s ease;
        display: flex;
        flex-direction: column;
        align-items: center;
    }

    .menu-item:hover {
        transform: translateY(-10px);
        box-shadow: 0 15px 35px rgba(0,0,0,0.1);
        border-color: #d4af37; /* Toque de dourado para sofisticação */
    }

    .menu-item i {
        font-size: 45px;
        margin-bottom: 15px;
    }

    /* Cores e Ícones Específicos */
    .icon-cadastro { color: #34495e; }
    
    /* Ícone Financeiro: 'Landmark' ou 'Chart-Line' para sofisticação */
    .icon-financeiro { color: #1e555c; }

    .menu-label {
        font-weight: 600;
        font-size: 1.1rem;
        letter-spacing: 0.5px;
    }
</style>

<div class="main-container">
    <img src="https://i.imgur.com/vHq0AUP.png" class="logo-zion" alt="Logo Zion">

    <div class="nav-grid">
        
        <a href="/cadastro" target="_self" class="menu-item">
            <i class="fas fa-user-check icon-cadastro"></i>
            <span class="menu-label">Cadastro</span>
        </a>

        <a href="/financeiro" target="_self" class="menu-item">
            <i class="fas fa-balance-scale-left icon-financeiro"></i>
            <span class="menu-label">Financeiro</span>
        </a>

    </div>
</div>
"""

# Comando para renderizar o Menu no Streamlit
st.markdown(MENU_HTML, unsafe_allow_html=True)</div></div></div># ============================================================
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
