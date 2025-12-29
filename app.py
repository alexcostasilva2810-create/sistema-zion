import streamlit as st
import pandas as pd

# Configuração visual profissional
st.set_page_config(page_title="ZION TECNOLOGIA", layout="wide")

# Estilo para botões e cores da marca
st.markdown("""
    <style>
    .stButton>button { width: 100%; background-color: #007bff; color: white; }
    [data-testid="stSidebar"] { background-color: #f8f9fa; }
    </style>
    """, unsafe_allow_html=True)

# --- MENU LATERAL COM ÍCONES ---
st.sidebar.markdown("<h2 style='color: #007bff; text-align: center;'>ZION</h2>", unsafe_allow_html=True)
escolha = st.sidebar.radio("Navegação", ["🏠 Início (Capa)", "📝 Novo Cadastro", "💰 Financeiro", "📊 Gráficos"])

# --- TELA 1: CAPA ---
if escolha == "🏠 Início (Capa)":
    st.markdown("<h1 style='text-align: center;'>ZION TECNOLOGIA</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>Gestão de Vigilância e Escolta</h3>", unsafe_allow_html=True)
    st.divider()
    st.image("https://via.placeholder.com/800x300/007bff/ffffff?text=SISTEMA+DE+GESTÃO+ZION", use_container_width=True)

# --- TELA 2: FORMULÁRIO DE PREENCHIMENTO ---
elif escolha == "📝 Novo Cadastro":
    st.title("📝 Cadastro de Nova O.S")
    with st.form("meu_formulario", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("Número da O.S")
            st.date_input("Data do Serviço")
            st.selectbox("Motorista", ["SAMUEL PONTES", "RODRIGO SANTANA", "JOÃO DIAS"])
        with col2:
            st.text_input("Local de Origem/Destino")
            st.number_input("Valor Bruto (R$)", format="%.2f")
            st.number_input("Soma de Despesas (R$)", format="%.2f")
        
        st.form_submit_button("SALVAR DADOS NO SISTEMA")

# --- TELA 3: FINANCEIRO ---
elif escolha == "💰 Financeiro":
    st.title("💰 Controle Financeiro")
    st.metric("Faturamento Total Mensal", "R$ 15.400,00", "+5%")
    # Tabela simulada
    df_exemplo = pd.DataFrame({
        'DATA': ['29/12/2025', '28/12/2025'],
        'MOTORISTA': ['SAMUEL PONTES', 'RODRIGO SANTANA'],
        'VALOR': [740.00, 1210.00],
        'STATUS': ['FINALIZADO', 'EM ANDAMENTO']
    })
    st.table(df_exemplo)
