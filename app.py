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
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap" rel="stylesheet">

<style>
    :root {
        --primary-color: #1a237e; /* Azul Sofisticado Zion */
        --bg-color: #f4f7f6;
        --card-white: #ffffff;
    }

    .zion-dashboard {
        font-family: 'Inter', sans-serif;
        display: flex;
        flex-direction: column;
        align-items: center;
        padding: 50px 20px;
        background-color: var(--bg-color);
        min-height: 100vh;
    }

    .zion-logo-container {
        margin-bottom: 50px;
        text-align: center;
    }

    /* Estilo para a Logo (ajustado para não quebrar se a imagem sumir) */
    .zion-logo-img {
        max-width: 220px;
        height: auto;
        display: block;
    }

    .nav-grid- Zion {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
        gap: 20px;
        width: 100%;
        max-width: 700px;
    }

    .menu-card {
        background: var(--card-white);
        text-decoration: none;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 30px 20px;
        border-radius: 16px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        border: 1px solid rgba(0,0,0,0.03);
    }

    .menu-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 12px 24px rgba(0,0,0,0.1);
        border-color: var(--primary-color);
    }

    /* Estilo dos Ícones */
    .menu-card i {
        font-size: 36px;
        margin-bottom: 15px;
    }

    /* Ícone Cadastro - Corrigido */
    .icon-reg { color: #546e7a; }
    
    /* Ícone Financeiro - Sofisticado (Gráfico de colunas com tendência) */
    .icon-fin { color: #2e7d32; }

    .menu-label {
        font-size: 15px;
        font-weight: 600;
        color: #333;
        letter-spacing: 0.3px;
    }
</style>

<div class="zion-dashboard">
    
    <div class="zion-logo-container">
        <img src="https://via.placeholder.com/220x80?text=ZION+LOGO" alt="Zion Business" class="zion-logo-img">
    </div>

    <div class="nav-grid-Zion">
        
        <a href="SUA_URL_DE_CADASTRO_AQUI" class="menu-card">
            <i class="fas fa-id-card-alt icon-reg"></i>
            <span class="menu-label">Cadastro</span>
        </a>

        <a href="SUA_URL_DE_FINANCEIRO_AQUI" class="menu-card">
            <i class="fas fa-chart-pie icon-fin"></i>
            <span class="menu-label">Financeiro</span>
        </a>

        <a href="#" class="menu-card">
            <i class="fas fa-users-cog" style="color: #607d8b;"></i>
            <span class="menu-label">Gestão</span>
        </a>

    </div>
</div></div># ============================================================
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
