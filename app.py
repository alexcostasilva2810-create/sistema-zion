import streamlit as st

# Configuração da Página
st.set_page_config(page_title="ZION TECNOLOGIA", layout="wide")

# --- ESTADO DO SISTEMA (MEMÓRIA) ---
if 'pagina' not in st.session_state:
    st.session_state.pagina = "🏠 Início"
if 'empurradores' not in st.session_state:
    st.session_state.empurradores = ["SAMUEL PONTES", "RODRIGO SANTANA", "JOÃO DIAS"]

# --- BARRA LATERAL (LOGO NAVEGÁVEL) ---
with st.sidebar:
    # Ao clicar na imagem, ela muda o estado da página para Início
    if st.button("🏠 VOLTAR AO INÍCIO", use_container_width=True):
        st.session_state.pagina = "🏠 Início"
    
    st.image("logo.png", use_container_width=True)
    st.markdown("<h2 style='text-align: center;'>ZION</h2>", unsafe_allow_html=True)
    st.divider()
    
    # Menu de Navegação
    escolha = st.radio("Selecione a opção:", ["🏠 Início", "📝 Nova O.S", "👥 Cadastrar Empurrador", "💰 Financeiro"])
    st.session_state.pagina = escolha

# --- TELA 1: INÍCIO (CAPA) ---
if st.session_state.pagina == "🏠 Início":
    st.markdown("<h1 style='text-align: center;'>ZION TECNOLOGIA</h1>", unsafe_allow_html=True)
    st.divider()
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.image("logo.png", use_container_width=True)
        st.markdown("<h3 style='text-align: center;'>Gestão de Vigilância e Escolta</h3>", unsafe_allow_html=True)

# --- TELA 2: FORMULÁRIO (ORDEM EXATA DO VÍDEO) ---
elif st.session_state.pagina == "📝 Nova O.S":
    st.title("📝 Formulário de Ordem de Serviço")
    
    with st.form("form_os", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            pedido = st.text_input("PEDIDO")
            # O número da O.S uma vez criado é salvo e não muda
            os_num = st.number_input("NÚMERO DA O.S", min_value=0, step=1)
            data_inicio = st.date_input("INÍCIO DA MISSÃO")
            hora_embarque = st.text_input("HORA DO EMBARQUE")
            local = st.text_input("LOCAL")

        with col2:
            # Lista suspensa dinâmica que você gerencia
            empurrador = st.selectbox("EMPURRADOR", st.session_state.empurradores)
            cmt = st.text_input("CMT")
            saida = st.text_input("SAÍDA")
            data_fim = st.date_input("FIM DA MISSÃO")
            hora_termino = st.text_input("HORA/TÉRMINO DA MISSÃO")

        st.divider()
        c3, c4 = st.columns(2)
        with c3:
            escolta1 = st.text_input("ESCOLTA 1")
            status = st.radio("STATUS", ["ANDAMENTO", "ENCERRADO"], horizontal=True)
        with c4:
            escolta2 = st.text_input("ESCOLTA 2")
            retroativo = st.radio("RETROATIVO", ["R", "FINALIZADO"], horizontal=True)

        if st.form_submit_button("CONCLUIR CADASTRO"):
            st.success(f"O.S {os_num} cadastrada com sucesso!")

# --- TELA 3: GERENCIAR EMPURRADORES ---
elif st.session_state.pagina == "👥 Cadastrar Empurrador":
    st.title("👥 Gerenciar Lista de Empurradores")
    novo_nome = st.text_input("Digite o nome completo para a lista suspensa:").upper()
    if st.button("Adicionar à Lista"):
        if novo_nome and novo_nome not in st.session_state.empurradores:
            st.session_state.empurradores.append(novo_nome)
            st.success(f"O nome {novo_nome} agora aparecerá no formulário!")
            st.rerun()
