import streamlit as st
import requests
import pandas as pd
from fpdf import FPDF
from datetime import datetime
import io

# ============================================================
# # ........ CONFIGURAÇÕES E MOTOR ........ #
# ============================================================
st.set_page_config(page_title="Zion Tecnologia", layout="wide", initial_sidebar_state="collapsed")

if 'pagina' not in st.session_state:
    st.session_state.pagina = "🏠 HOME"

def navegar(destino):
    st.session_state.pagina = destino
    st.rerun()

# --- Estilo Visual para Smartphone ---
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #001a4d 0%, #003399 100%); }
    h1, h2, h3, p, span, label { color: white !important; }
    .stButton>button { 
        width: 100%; border-radius: 12px; height: 3.5em; 
        font-weight: bold; background-color: white !important; color: #001a4d !important;
        border: none; box-shadow: 0px 4px 10px rgba(0,0,0,0.3);
    }
    .card {
        background: rgba(255, 255, 255, 0.1);
        padding: 20px; border-radius: 15px; border: 1px solid rgba(255, 255, 255, 0.2);
        text-align: center; margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# ============================================================
# # ........ BLOCO: HOME (MENU PRINCIPAL) ........ #
# ============================================================
if st.session_state.pagina == "🏠 HOME":
    st.markdown("<h1 style='text-align: center;'>ZION TECNOLOGIA</h1>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,1,1])
    
    with col1:
        st.markdown('<div class="card">📝<br><h3>CADASTRO</h3></div>', unsafe_allow_html=True)
        if st.button("NOVO REGISTRO", key="h1"): navegar("📋 CADASTRO")
            
    with col2:
        st.markdown('<div class="card">📅<br><h3>GRADE</h3></div>', unsafe_allow_html=True)
        if st.button("VER O.S", key="h2"): navegar("📊 GRADE")
            
    with col3:
        st.markdown('<div class="card">💰<br><h3>FINANCEIRO</h3></div>', unsafe_allow_html=True)
        if st.button("ESTRATÉGICO", key="h3"): navegar("💰 FINANCEIRO")

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
