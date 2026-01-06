import streamlit as st

# 1. Configuração inicial da página
st.set_page_config(page_title="Zion Tecnologia", layout="centered")

# 2. Lógica de navegação simples
if 'pagina' not in st.session_state:
    st.session_state.pagina = 'inicio'

def mudar_pagina(nome):
    st.session_state.pagina = nome

# 3. CSS SEGURO (Onde estava o erro)
# Agora envolvido corretamente para o Python não travar
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: white;
        border: 1px solid #ddd;
    }
    [data-testid="stVerticalBlock"] > div:first-child {
        cursor: pointer;
    }
    </style>
    """, unsafe_allow_html=True)

# --- INTERFACE ---

# Botão Auxiliar de Topo (Opcional, conforme solicitado)
col_vazia, col_btn = st.columns([3, 1])
with col_btn:
    if st.button("☰ ÍCONES OPERACIONAIS"):
        mudar_pagina('menu')

# TELA DE MENU (Ícones Operacionais)
if st.session_state.pagina == 'menu':
    st.title("⚙️ Operacional")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📋 NOVO LANÇAMENTO"):
            st.success("Acessando Novo Lançamento...")
    with col2:
        if st.button("📊 VER AGENDAMENTO"):
            mudar_pagina('inicio')
    with col3:
        if st.button("💰 FINANCEIRO"):
            st.success("Acessando Financeiro...")
            
    if st.button("← VOLTAR"):
        mudar_pagina('inicio')

# TELA DE INÍCIO (A que você gosta com a Logo)
else:
    # Mostra a logo centralizada
    # Certifique-se de que o arquivo 'logo.png' está na mesma pasta do app.py
    try:
        st.image("logo.png", use_container_width=True)
    except:
        st.info("ZION TECNOLOGIA (Clique na logo para acessar)")

    # Se você clicar na logo (ou quiser o botão de acesso abaixo)
    if st.button("ACESSAR SISTEMA"):
        mudar_pagina('menu')

    st.divider()
    
    # Tabela simples e limpa para evitar novos erros
    st.subheader("📋 Agendamentos")
    st.write("Nenhum agendamento para hoje.")
