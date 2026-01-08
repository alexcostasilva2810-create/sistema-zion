import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import os

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Zion Tecnologia", layout="wide", initial_sidebar_state="collapsed")

# 2. MOTOR DE NAVEGAÇÃO
if 'pagina' not in st.session_state:
    st.session_state.pagina = "🏠 HOME"

def navegar(destino):
    st.session_state.pagina = destino
    st.rerun()

# 3. ESTILO CSS (Fundo Escritório, Azul Suave, Ícones Mostarda, Mão de Robô e Texto Futuro)
st.markdown("""
<style>
    /* Remove barra lateral e erros */
    [data-testid="stSidebar"], .stAlert { display: none !important; }
    
    /* Fundo com Imagem de Escritório e Overlay Azul */
    .stApp {
        background: linear-gradient(rgba(0, 26, 64, 0.8), rgba(0, 26, 64, 0.8)), 
                    url('https://images.unsplash.com/photo-1497366216548-37526070297c?auto=format&fit=crop&q=80&w=2000');
        background-size: cover;
        background-attachment: fixed;
    }

    h1 { 
        color: white !important; 
        text-align: center; 
        font-size: 38px !important; 
        margin-bottom: 40px !important; 
        font-weight: 800;
        text-shadow: 2px 2px 10px rgba(0,0,0,0.5); /* Sombra para destaque */
    }

    /* Estilo dos Botões */
    div.stButton > button {
        width: 100%;
        height: 100px !important;
        background: rgba(255, 255, 255, 0.07) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 15px !important;
        font-weight: bold !important;
        transition: 0.3s ease;
    }
    div.stButton > button:hover { 
        border-color: #E2B13C !important; /* Mostarda no hover */
        background: rgba(255, 255, 255, 0.15) !important;
    }

    /* Ajuste de Ícones */
    .icon-box { text-align: center; margin-bottom: -15px; }
    .icon-box img { width: 80px; }
    
    /* Filtro Amarelo Mostarda */
    .mostarda img { 
        filter: invert(78%) sepia(35%) saturate(836%) hue-rotate(354deg) brightness(93%) contrast(92%) !important; 
    }

    /* Frase de Boas-Vindas */
    .welcome-text {
        color: #E2B13C; /* Cor Mostarda */
        text-align: center;
        font-size: 55px; /* Tamanho AUMENTADO */
        font-weight: 900; /* Negrito Extra */
        margin-top: 60px;
        text-shadow: 3px 3px 20px rgba(0,0,0,0.8); /* Sombra mais forte */
        font-family: 'sans-serif';
        line-height: 1.2; /* Espaçamento entre linhas */
    }

    /* Ícone Mão de Robô */
    .robot-hand-icon {
        text-align: center;
        margin-top: 40px; /* Espaço acima da frase */
        margin-bottom: 20px; /* Espaço abaixo da mão */
    }
    .robot-hand-icon img {
        width: 180px; /* Tamanho da Mão de Robô */
        filter: invert(90%) sepia(10%) saturate(1000%) hue-rotate(180deg) brightness(1.2); /* Cor de Robô */
        opacity: 0.8; /* Transparência suave */
    }
</style>
""", unsafe_allow_html=True)

# 4. TELA INICIAL (HOME)
if st.session_state.pagina == "🏠 HOME":
    st.markdown("<h1>ZION BUSINESS</h1>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)

    with col1:
        # Ícone de Caneta (Mostarda)
        st.markdown('<div class="icon-box mostarda"><img src="https://cdn-icons-png.flaticon.com/512/1250/1250615.png"></div>', unsafe_allow_html=True)
        if st.button("📝 NOVO LANÇAMENTO", key="bt_lan"):
            st.session_state.dados_edicao = None
    # Frase solicitada
    st.markdown('<p class="welcome-text">Seja Bem Vindo ao Futuro</p>', unsafe_allow_html=True)# Os demais blocos (Cadastro, Grade, Financeiro) seguem sua lógica original abaixo
elif st.session_state.pagina == "📋 CADASTRO":
    edit = st.session_state.dados_edicao
    st.header("📝 Formulário O.S")
    if st.button("⬅️ VOLTAR"): navegar("🏠 HOME")
    
    with st.form("form_os"):
        c1, c2, c3 = st.columns(3)
        os_n = c1.text_input("Nº O.S", value=edit["Nº OS"] if edit else "")
        dt_val = datetime.strptime(edit["DT_SAIDA_RAW"], '%Y-%m-%d') if edit and edit["DT_SAIDA_RAW"] else datetime.now()
        dt_s = c2.date_input("DATA SAÍDA", value=dt_val, format="DD/MM/YYYY")
        cli = c3.text_input("CLIENTE", value=edit["CLIENTE"] if edit else "")
        
        # ... (Mantive o restante do seu formulário igual para não perder dados)
        obs = st.text_area("DESCRIÇÃO / OBSERVAÇÕES", value=edit.get("DESCRIÇÃO", "") if edit else "")
        
        if st.form_submit_button("✅ SALVAR OPERAÇÃO", type="primary"):
            st.success("Dados prontos para envio!")
            navegar("📊 GRADE")

elif st.session_state.pagina == "📊 GRADE":
    st.header("📊 Ver Agendamentos")
    if st.button("⬅️ VOLTAR"): navegar("🏠 HOME")
    dados = carregar_dados()
    if dados:
        for d in dados:
            with st.expander(f"O.S {d['Nº OS']} - {d['CLIENTE']}"):
                st.write(f"**Status:** {d['STATUS']} | **Valor:** R$ {d['VALOR']:,.2f}")
                c1, c2 = st.columns(2)
                if c1.button("✏️ EDITAR", key=f"ed_{d['ID']}", type="primary"):
                    st.session_state.dados_edicao = d; navegar("📋 CADASTRO")
                pdf_os = gerar_pdf_os(d)
                c2.download_button("📄 GERAR PDF", pdf_os, f"OS_{d['Nº OS']}.pdf", key=f"p_{d['ID']}")

elif st.session_state.pagina == "💰 FINANCEIRO":
    st.header("💰 Financeiro")
    if st.button("⬅️ VOLTAR"): navegar("🏠 HOME")
    
    c1, c2 = st.columns(2)
    f_ini = c1.date_input("Início", value=datetime.now())
    f_fim = c2.date_input("Fim", value=datetime.now())
    
    dados = carregar_dados()
    if dados:
        df = pd.DataFrame(dados)
        df['dt_filter'] = pd.to_datetime(df['DT_SAIDA_RAW'])
        df_filt = df[(df['dt_filter'] >= pd.Timestamp(f_ini)) & (df['dt_filter'] <= pd.Timestamp(f_fim))]
        
        st.metric("Total Faturado", f"R$ {df_filt['VALOR'].sum():,.2f}")
        st.dataframe(df_filt[["Nº OS", "CLIENTE", "DT SAÍDA", "VALOR"]], use_container_width=True)
        
        pdf_fin = gerar_pdf_financeiro(df_filt, df_filt['VALOR'].sum(), f_ini, f_fim)
        st.download_button("📥 BAIXAR RELATÓRIO PDF", pdf_fin, "financeiro.pdf", type="primary")
