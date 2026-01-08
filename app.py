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
 unsafe_allow_html=True)
# ============================================================
# # ........ BLOCO: HOME (MENU PRINCIPAL) ........ #
# ============================================================
# --- Definição do Menu (Coloque isso antes do bloco if/elif) ---
# Usamos aspas triplas """ para que o Python ignore o CSS lá dentro
MENU_HOME = """
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">

<style>
    .main-wrapper {
        display: flex;
        flex-direction: column;
        align-items: center;
        padding: 40px 10px; /* O erro estava aqui, agora está protegido por aspas */
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    .logo-zion {
        width: 180px;
        margin-bottom: 40px;
        transition: 0.3s;
    }

    .menu-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 20px;
        width: 100%;
        max-width: 400px;
    }

    .menu-card {
        background: #ffffff;
        border-radius: 15px;
        padding: 25px;
        text-align: center;
        text-decoration: none;
        color: #333;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        border: 1px solid #eee;
        transition: all 0.3s ease;
    }

    .menu-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.15);
        border-color: #1a237e;
    }

    .menu-card i {
        font-size: 40px;
        margin-bottom: 15px;
        display: block;
    }

    /* Cores dos Ícones */
    .icon-cadastro { color: #455a64; }
    .icon-financeiro { color: #004d40; } /* Verde escuro sofisticado */

    .label {
        font-weight: bold;
        font-size: 16px;
    }
</style>

<div class="main-wrapper">
    <img src="https://SUA_URL_DA_LOGO_AQUI.png" class="logo-zion" alt="Zion Logo">

    <div class="menu-grid">
        <a href="?pagina=CADASTRO" class="menu-card">
            <i class="fas fa-user-plus icon-cadastro"></i>
            <span class="label">Cadastro</span>
        </a>

        <a href="?pagina=FINANCEIRO" class="menu-card">
            <i class="fas fa-chart-line icon-financeiro"></i>
            <span class="label">Financeiro</span>
        </a>
    </div>
</div>
"""

# --- Lógica de Exibição (Onde estava o erro de sintaxe) ---
if st.session_state.pagina == "🏠 HOME":
    st.markdown(MENU_HOME, unsafe_allow_html=True)

elif st.session_state.pagina == "📋 CADASTRO":
    # Seu código de cadastro aqui...
    st.markdown("<h1>Página de Cadastro</h1>", unsafe_allow_html=True)
    if st.button("Voltar"):
        st.session_state.pagina = "🏠 HOME"
        st.rerun()# ============================================================
# # ........ BLOCO: CADASTRO (REGISTRO) ........ #
# ============================================================
elif st.session_state.pagina == "📋 CADASTRO":
    st.markdown("<h1>📋 NOVO LANÇAMENTO</h1>", unsafe_allow_html=True)
    
    # Verifique se a função navegar está definida antes deste bloco
    if st.button("⬅️ VOLTAR PARA HOME", key="c1"):
        navegar("🏠 HOME")    
    
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
