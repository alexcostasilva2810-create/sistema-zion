import streamlit as st
import os

# Configuração da página
st.set_page_config(page_title="ZION TECNOLOGIA", layout="wide")

# Gerenciamento da lista de empurradores
if 'lista_empurradores' not in st.session_state:
    st.session_state.lista_empurradores = ["SAMUEL PONTES", "RODRIGO SANTANA", "JOÃO DIAS"]

# Função para encontrar a logo (não importa se é logo.png ou LOGO.PNG)
def buscar_logo():
    arquivos = os.listdir('.')
    for f in arquivos:
        if f.lower() == "logo.png":
            return f
    return None

logo_encontrada = buscar_logo()

# --- MENU LATERAL ---
with st.sidebar:
    if logo_encontrada:
        st.image(logo_encontrada, use_container_width=True)
    else:
        st.error("Renomeie o arquivo no GitHub para: logo.png")
    
    st.markdown("<h2 style='text-align: center;'>SISTEMA ZION</h2>", unsafe_allow_html=True)
    aba = st.radio("Navegação", ["🏠 Início", "📝 Nova O.S", "👥 Gerenciar Nomes"])

# --- TELA 1: INÍCIO ---
if aba == "🏠 Início":
    st.markdown("<h1 style='text-align: center;'>ZION TECNOLOGIA</h1>", unsafe_allow_html=True)
    st.divider()
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        if logo_encontrada:
            st.image(logo_encontrada, use_container_width=True)
        st.markdown("<h3 style='text-align: center;'>Controle de Vigilância</h3>", unsafe_allow_html=True)

# --- TELA 2: FORMULÁRIO (CONFORME O VÍDEO) ---
elif aba == "📝 Nova O.S":
    st.title("📝 Cadastro de Missão")
    with st.form("form_os", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            pedido = st.text_input("PEDIDO")
            # O número da O.S uma vez preenchido e salvo não pode ser editado
            os_num = st.number_input("NÚMERO DA O.S", min_value=1, step=1)
            data_inicio = st.date_input("DATA INÍCIO")
            local = st.text_input("LOCAL")
        with c2:
            # Lista suspensa dinâmica que você alimenta
            empurrador = st.selectbox("EMPURRADOR", st.session_state.lista_empurradores)
            cmt = st.text_input("CMT")
            saida = st.text_input("SAÍDA")
            status = st.selectbox("STATUS", ["ANDAMENTO", "ENCERRADO"])

        if st.form_submit_button("SALVAR E BLOQUEAR O.S"):
            st.success(f"O.S {os_num} salva com sucesso e bloqueada para alteração!")

# --- TELA 3: CADASTRO DE NOMES ---
elif aba == "👥 Gerenciar Nomes":
    st.title("👥 Adicionar à Lista Suspensa")
    novo = st.text_input("Novo nome:").upper()
    if st.button("Salvar na Lista"):
        if novo and novo not in st.session_state.lista_empurradores:
            st.session_state.lista_empurradores.append(novo)
            st.success(f"{novo} adicionado!")
            st.rerun()
