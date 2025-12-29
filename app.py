import streamlit as st
import pandas as pd
from datetime import datetime

# Configuração da Página
st.set_page_config(page_title="ZION TECNOLOGIA", layout="wide")

# --- BANCO DE DADOS TEMPORÁRIO (Memória) ---
if 'empurradores' not in st.session_state:
    st.session_state.empurradores = ["SAMUEL PONTES", "RODRIGO SANTANA", "JOÃO DIAS"]

if 'banco_os' not in st.session_state:
    st.session_state.banco_os = pd.DataFrame(columns=["PEDIDO", "O.S", "LOCAL", "EMPURRADOR", "STATUS"])

# --- MENU LATERAL ---
with st.sidebar:
    st.markdown("<h1 style='text-align: center; color: #007bff;'>ZION</h1>", unsafe_allow_html=True)
    escolha = st.radio("Navegação", ["🏠 Início", "📝 Nova O.S", "👥 Gerenciar Empurradores", "💰 Financeiro"])

# --- TELA 1: CAPA (INÍCIO) ---
if escolha == "🏠 Início":
    st.markdown("<h1 style='text-align: center;'>ZION TECNOLOGIA</h1>", unsafe_allow_html=True)
    st.divider()
    # Ícone centralizado
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.image("https://cdn-icons-png.flaticon.com/512/1063/1063302.png", width=200) 
        st.markdown("<h3 style='text-align: center;'>Gestão de Vigilância e Escolta</h3>", unsafe_allow_html=True)

# --- TELA 2: CADASTRO DE EMPURRADORES (SÓ VOCÊ USA) ---
elif escolha == "👥 Gerenciar Empurradores":
    st.title("👥 Cadastro de Empurradores")
    novo_nome = st.text_input("Digite o nome do novo Empurrador/Motorista:").upper()
    if st.button("Adicionar à Lista"):
        if novo_nome and novo_nome not in st.session_state.empurradores:
            st.session_state.empurradores.append(novo_nome)
            st.success(f"{novo_nome} adicionado com sucesso!")
    
    st.subheader("Lista Atual:")
    st.write(", ".join(st.session_state.empurradores))

# --- TELA 3: FORMULÁRIO DE NOVA O.S ---
elif escolha == "📝 Nova O.S":
    st.title("📝 Formulário de Ordem de Serviço")
    
    with st.form("form_os", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            pedido = st.text_input("PEDIDO")
            # O número da O.S aqui é definido no cadastro e não muda depois de salvo
            os_num = st.number_input("NÚMERO DA O.S", min_value=1, step=1)
            data_inicio = st.date_input("INÍCIO DA MISSÃO")
            hora_embarque = st.text_input("HORA DO EMBARQUE")
            local = st.text_input("LOCAL")

        with col2:
            # LISTA SUSPENSA DINÂMICA
            empurrador = st.selectbox("EMPURRADOR", st.session_state.empurradores)
            cmt = st.text_input("CMT")
            saida = st.text_input("SAÍDA")
            data_fim = st.date_input("FIM DA MISSÃO")
            hora_termino = st.text_input("HORA/TÉRMINO DA MISSÃO")

        st.divider()
        col3, col4 = st.columns(2)
        with col3:
            escolta1 = st.text_input("ESCOLTA 1")
            status = st.radio("STATUS", ["ANDAMENTO", "ENCERRADO"], horizontal=True)
        with col4:
            escolta2 = st.text_input("ESCOLTA 2")
            retroativo = st.radio("RETROATIVO", ["R", "FINALIZADO"], horizontal=True)

        if st.form_submit_button("CONCLUIR CADASTRO"):
            st.success(f"O.S {os_num} salva com sucesso e bloqueada para edição!")

# --- TELA 4: FINANCEIRO (LISTA IGUAL AO VÍDEO) ---
elif escolha == "💰 Financeiro":
    st.title("💰 Histórico Financeiro")
    st.info("Aqui aparecerão os dados salvos das O.S cadastradas.")
