import streamlit as st

# Configuração da Página
st.set_page_config(page_title="ZION TECNOLOGIA", layout="wide")

# --- BANCO DE DADOS EM MEMÓRIA (LISTA DE EMPURRADORES) ---
if 'empurradores' not in st.session_state:
    st.session_state.empurradores = ["SAMUEL PONTES", "RODRIGO SANTANA", "JOÃO DIAS"]

# --- MENU LATERAL ---
with st.sidebar:
    # Tenta carregar a imagem que você acabou de subir
    try:
        st.image("logo.png", use_container_width=True)
    except:
        st.error("Arquivo logo.png não encontrado no GitHub.")
    
    st.markdown("<h2 style='text-align: center; color: #007bff;'>SISTEMA GESTÃO</h2>", unsafe_allow_html=True)
    escolha = st.radio("Navegação", ["🏠 Início (Capa)", "📝 Novo Cadastro", "👥 Gerenciar Empurradores"])

# --- TELA 1: CAPA ---
if escolha == "🏠 Início (Capa)":
    st.markdown("<h1 style='text-align: center;'>ZION TECNOLOGIA</h1>", unsafe_allow_html=True)
    st.divider()
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.image("logo.png", use_container_width=True)
        st.markdown("<h3 style='text-align: center;'>Gestão de Vigilância e Escolta</h3>", unsafe_allow_html=True)

# --- TELA 2: FORMULÁRIO (SEQUÊNCIA DO VÍDEO) ---
elif escolha == "📝 Novo Cadastro":
    st.title("📝 Cadastro de Ordem de Serviço")
    with st.form("form_os", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            pedido = st.text_input("PEDIDO")
            # O número da O.S não pode ser editado em uma planilha, aqui ele é fixo no envio
            os_num = st.number_input("NÚMERO DA O.S", min_value=1, step=1)
            data_inicio = st.date_input("INÍCIO DA MISSÃO")
            hora_embarque = st.text_input("HORA DO EMBARQUE")
            local = st.text_input("LOCAL")

        with col2:
            # Lista suspensa que você alimenta
            empurrador = st.selectbox("EMPURRADOR", st.session_state.empurradores)
            cmt = st.text_input("CMT")
            saida = st.text_input("SAÍDA")
            data_fim = st.date_input("FIM DA MISSÃO")
            hora_termino = st.text_input("HORA/TÉRMINO DA MISSÃO")

        st.divider()
        if st.form_submit_button("CONCLUIR E BLOQUEAR O.S"):
            st.success(f"O.S {os_num} registrada com sucesso!")

# --- TELA 3: GERENCIAR LISTA ---
elif escolha == "👥 Gerenciar Empurradores":
    st.title("👥 Gerenciar Lista de Nomes")
    novo_nome = st.text_input("Nome do novo colaborador:").upper()
    if st.button("Adicionar à Lista"):
        if novo_nome and novo_nome not in st.session_state.empurradores:
            st.session_state.empurradores.append(novo_nome)
            st.success("Nome adicionado com sucesso!")    st.write("Nomes atuais na lista:", st.session_state.lista_empurradores)
