import streamlit as st

# 1. Configuração inicial
st.set_page_config(page_title="Zion Tecnologia", layout="centered")

# 2. CSS Blindado para as Colunas aparecerem (Corrigindo o SyntaxError)
st.markdown("""
    <style>
    /* Estilo para a Tabela com Bordas Pretas e Visíveis */
    .grade-zion {
        width: 100%;
        border-collapse: collapse;
        background-color: white;
        color: black;
    }
    .grade-zion th {
        border: 2px solid #000000 !important;
        background-color: #f0f2f6;
        padding: 10px;
        text-align: left;
    }
    .grade-zion td {
        border: 2px solid #000000 !important;
        padding: 10px;
    }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Lógica de Navegação
if 'pagina' not in st.session_state:
    st.session_state.pagina = 'inicio'

def navegar(nome):
    st.session_state.pagina = nome

# --- BOTÃO AUXILIAR NO TOPO ---
col_vazia, col_btn_top = st.columns([3, 1])
with col_btn_top:
    if st.button("☰ OPERACIONAL"):
        navegar('menu')

# --- TELA DE MENU (ÍCONES) ---
if st.session_state.pagina == 'menu':
    st.markdown("## ⚙️ Painel Operacional")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📋 NOVO LANÇAMENTO"):
            st.info("Acessando Novo Lançamento...")
    with col2:
        if st.button("📊 AGENDAMENTOS"):
            navegar('inicio')
    with col3:
        if st.button("💰 FINANCEIRO"):
            st.info("Acessando Financeiro...")
    
    if st.button("← VOLTAR PARA O INÍCIO"):
        navegar('inicio')

# --- TELA DE INÍCIO (LOGO E TABELA COM COLUNAS) ---
else:
    # Logo centralizada
    try:
        st.image("logo.png", use_container_width=True)
    except:
        st.markdown("<h1 style='text-align: center;'>ZION TECNOLOGIA</h1>", unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("📅 Grade de Agendamentos")

    # AQUI ESTÁ A SOLUÇÃO PARA AS COLUNAS APARECEREM
    st.markdown("""
        <table class="grade-zion">
            <thead>
                <tr>
                    <th>HORÁRIO</th>
                    <th>CLIENTE</th>
                    <th>SERVIÇO</th>
                    <th>STATUS</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td colspan="4" style="text-align:center; padding: 40px; color: gray;">
                        Nenhum agendamento registrado. As colunas acima estão prontas.
                    </td>
                </tr>
            </tbody>
        </table>
        """, unsafe_allow_html=True)
