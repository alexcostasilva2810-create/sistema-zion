import streamlit as st
import pandas as pd

# Configuração da Página
st.set_page_config(page_title="ZION TECNOLOGIA", layout="wide")

# --- GERENCIAMENTO DE DADOS (ESTADO DO APP) ---
if 'lista_empurradores' not in st.session_state:
    st.session_state.lista_empurradores = ["SAMUEL PONTES", "RODRIGO SANTANA", "JOÃO DIAS"]

# --- FUNÇÃO PARA VOLTAR AO INÍCIO AO CLICAR NA LOGO ---
def voltar_inicio():
    st.session_state.pagina = "🏠 Início"

if 'pagina' not in st.session_state:
    st.session_state.pagina = "🏠 Início"

# --- MENU LATERAL ---
with st.sidebar:
    # Sua Logo como botão navegável
    st.image("https://raw.githubusercontent.com/alexcostasilva2810-criar/sistema-zion/main/logo.png") # Certifique-se de que o nome no GitHub é logo.png
    st.markdown("<h2 style='text-align: center; color: #007bff;'>SISTEMA GESTÃO</h2>", unsafe_allow_html=True)
    
    aba_selecionada = st.radio("Navegação", ["🏠 Início", "📝 Nova O.S", "👥 Cadastrar Empurrador", "💰 Financeiro"])
    st.session_state.pagina = aba_selecionada

# --- TELA 1: CAPA COM LOGO REAL ---
if st.session_state.pagina == "🏠 Início":
    st.markdown("<h1 style='text-align: center;'>ZION TECNOLOGIA</h1>", unsafe_allow_html=True)
    st.divider()
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        # Mostra sua logo grande na capa
        st.image("https://raw.githubusercontent.com/alexcostasilva2810-criar/sistema-zion/main/logo.png", use_container_width=True)
        st.markdown("<h3 style='text-align: center;'>Controle de Vigilância</h3>", unsafe_allow_html=True)

# --- TELA 2: FORMULÁRIO DE NOVA O.S (ORDEM DO VÍDEO) ---
elif st.session_state.pagina == "📝 Nova O.S":
    st.title("📝 Cadastro de Nova Missão")
    
    with st.form("form_os", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            pedido = st.text_input("PEDIDO")
            # Número da O.S - Uma vez definido aqui, ele será salvo no banco e não muda
            os_numero = st.number_input("NÚMERO DA O.S", min_value=1, step=1)
            data_inicio = st.date_input("INÍCIO DA MISSÃO")
            hora_embarque = st.text_input("HORA DO EMBARQUE")
            local = st.text_input("LOCAL")
        
        with col2:
            # Lista suspensa que você alimenta na outra aba
            empurrador = st.selectbox("EMPURRADOR", st.session_state.lista_empurradores)
            cmt = st.text_input("CMT")
            saida = st.text_input("SAÍDA")
            data_fim = st.date_input("FIM DA MISSÃO")
            hora_termino = st.text_input("HORA/TÉRMINO DA MISSÃO")

        st.divider()
        st.subheader("Equipe e Detalhes")
        c3, c4 = st.columns(2)
        with c3:
            escolta1 = st.text_input("ESCOLTA 1")
            status = st.radio("STATUS", ["ANDAMENTO", "ENCERRADO"], horizontal=True)
        with c4:
            escolta2 = st.text_input("ESCOLTA 2")
            retroativo = st.radio("RETROATIVO", ["R", "FINALIZADO"], horizontal=True)

        if st.form_submit_button("SALVAR E BLOQUEAR O.S"):
            st.success(f"O.S {os_numero} registrada com sucesso!")

# --- TELA 3: CADASTRO DE NOMES PARA A LISTA ---
elif st.session_state.pagina == "👥 Cadastrar Empurrador":
    st.title("👥 Gestão de Nomes (Empurradores)")
    novo_nome = st.text_input("Digite o nome completo:").upper()
    if st.button("Adicionar à Lista Suspensa"):
        if novo_nome and novo_nome not in st.session_state.lista_empurradores:
            st.session_state.lista_empurradores.append(novo_nome)
            st.success("Nome adicionado!")
    st.write("Nomes atuais na lista:", st.session_state.lista_empurradores)
