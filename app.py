import streamlit as st
import pandas as pd

# Configuração da página
st.set_page_config(page_title="ZION TECNOLOGIA", layout="wide")

# Menu Lateral
st.sidebar.markdown("<h1 style='text-align: center; color: #007bff;'>ZION</h1>", unsafe_allow_html=True)
escolha = st.sidebar.radio("Navegação", ["🏠 Início (Capa)", "📝 Novo Cadastro", "💰 Financeiro", "📊 Gráficos"])

# --- TELA DE INÍCIO (CAPA) ---
if escolha == "🏠 Início (Capa)":
    st.markdown("<h1 style='text-align: center;'>ZION TECNOLOGIA</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>Gestão de Vigilância e Escolta</h3>", unsafe_allow_html=True)
    st.divider()
    # Imagem de capa (Link atualizado para não quebrar)
    st.image("https://raw.githubusercontent.com/streamlit/docs/main/public/images/dashboards-hero.png", caption="Sistema de Gestão Zion", use_container_width=True)

# --- TELA DE CADASTRO (SEQUÊNCIA DO VÍDEO) ---
elif escolha == "📝 Novo Cadastro":
    st.title("📝 O.S Form")
    with st.form("form_os", clear_on_submit=True):
        # Sequência conforme o seu vídeo
        pedido = st.text_input("PEDIDO")
        os_numero = st.number_input("O.S", step=1)
        data_inicio = st.date_input("INÍCIO DA MISSÃO")
        hora_embarque = st.text_input("HORA DO EMBARQUE")
        local = st.text_input("LOCAL")
        empurrador = st.selectbox("EMPURRADOR", ["Opção 1", "Opção 2", "Opção 3"])
        cmt = st.text_input("CMT")
        saida = st.text_input("SAÍDA")
        data_fim = st.date_input("FIM DA MISSÃO")
        hora_termino = st.text_input("HORA/TÉRMINO DA MISSÃO")
        
        st.divider()
        escolta1 = st.text_input("ESCOLTA 1")
        escolta2 = st.text_input("ESCOLTA 2")
        descricao = st.text_area("DESCRIÇÃO")
        
        st.divider()
        status = st.radio("STATUS", ["ANDAMENTO", "ENCERRADO"])
        retroativo = st.radio("RETROATIVO", ["R", "FINALIZADO"])
        despesas = st.number_input("SOMA DE DESPESAS (R$)", format="%.2f")
        cliente = st.text_input("CLIENTE")
        destino = st.text_input("DESTINO")
        
        if st.form_submit_button("SALVAR O.S"):
            st.success("Dados salvos com sucesso!")

# --- OUTRAS TELAS ---
else:
    st.title(f"{escolha}")
    st.info("Área em desenvolvimento para conexão com banco de dados.")
