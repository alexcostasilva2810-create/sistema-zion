import streamlit as st
import pandas as pd
from datetime import datetime

# Configuração da página para esconder menus padrão e focar no sistema
st.set_page_config(page_title="ZION TECNOLOGIA", layout="wide", initial_sidebar_state="expanded")

# Estilização CSS para criar o visual de "App" com fundo escuro e cards
st.markdown("""
    <style>
    .main { background-color: #0c0f14; color: white; }
    [data-testid="stSidebar"] { background-color: #161b22; }
    .stButton>button { width: 100%; border-radius: 5px; background-color: #00acee; color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- MENU LATERAL COM ÍCONES ---
with st.sidebar:
    st.image("https://raw.githubusercontent.com/alexcostasilva2810-criar/sistema-zion/main/logo.png", width=200) # Substituiremos pela sua logo
    st.title("SISTEMA GESTÃO")
    escolha = st.radio("Selecione uma opção:", 
        ["🏠 Início", "📝 Novo Cadastro", "💰 Financeiro", "📊 Gráficos", "📋 Lista de O.S"])

# --- TELA 1: CAPA (INÍCIO) ---
if escolha == "🏠 Início":
    st.markdown("<h1 style='text-align: center;'>ZION TECNOLOGIA</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Controle de Vigilância e Gestão de Escolta</p>", unsafe_allow_html=True)
    
    # Grid de ícones decorativos no centro
    col1, col2, col3 = st.columns(3)
    with col1: st.info("🗓️ AGENDAMENTOS")
    with col2: st.info("📈 RELATÓRIOS")
    with col3: st.info("👥 MOTORISTAS")
    
    st.image("https://via.placeholder.com/800x300/161b22/00acee?text=BEM-VINDO+AO+APP+GESTÃO+DE+ESCOLTA", use_container_width=True)

# --- TELA 2: FORMULÁRIO DE PREENCHIMENTO ---
elif escolha == "📝 Novo Cadastro":
    st.title("📝 Preenchimento de Ordem de Serviço")
    
    with st.container():
        with st.form("form_registro", clear_on_submit=True):
            st.subheader("Informações da Missão")
            c1, c2, c3 = st.columns(3)
            num_os = c1.text_input("Número da O.S")
            data_missao = c2.date_input("Data da Missão")
            motorista = c3.selectbox("Motorista", ["SAMUEL PONTES", "RODRIGO SANTANA", "JOÃO DIAS", "LUZ FELIPE"])
            
            st.divider()
            st.subheader("Dados Financeiros")
            f1, f2, f3 = st.columns(3)
            valor_total = f1.number_input("Valor Total (R$)", min_value=0.0)
            debito = f2.number_input("Débito/Adiantamento (R$)", min_value=0.0)
            despesas = f3.number_input("Soma de Despesas (R$)", min_value=0.0)
            
            status = st.select_slider("Status do Serviço", options=["PROGRAMADO", "EM ANDAMENTO", "FINALIZADO"])
            
            enviar = st.form_submit_button("CONCLUIR CADASTRO")
            
            if enviar:
                st.success(f"O.S {num_os} registrada com sucesso no sistema!")

# --- TELA 3: FINANCEIRO (LISTA IGUAL AO VÍDEO) ---
elif escolha == "💰 Financeiro":
    st.title("💰 Painel Financeiro")
    # Aqui simulamos a visualização da tabela que aparece no vídeo
    dados_exemplo = {
        'ID': ['1.001', '1.002'],
        'MOTORISTA': ['SAMUEL PONTES', 'RODRIGO SANTANA'],
        'VALOR TOTAL': [740.00, 1210.00],
        'DÉBITO': [0.00, 150.00],
        'SOMA DESPESAS': [120.00, 300.00],
        'STATUS': ['ENCERRADO', 'EM ANDAMENTO']
    }
    st.dataframe(pd.DataFrame(dados_exemplo), use_container_width=True)
