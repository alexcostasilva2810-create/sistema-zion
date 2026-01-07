# --- ESTILO CSS (PLANO DE FUNDO E CENTRALIZAÇÃO) ---
st.markdown("""
    <style>
    /* Plano de fundo do sistema */
    .stApp {
        background: linear-gradient(135deg, #1e1e1e 0%, #2d2d2d 100%);
        background-attachment: fixed;
    }

    /* Estilização dos textos para ficarem legíveis no fundo escuro */
    h1, h2, h3, p, span, label {
        color: white !important;
    }

    /* Centralização da Logo */
    .centered-logo {
        display: flex;
        justify-content: center;
        margin-bottom: 20px;
    }

    /* Botão Verde Zion */
    div.stButton > button:first-child[kind="primary"] { 
        background-color: #28a745 !important; 
        color: white !important; 
        border: none;
    }
    
    .stButton>button { 
        width: 100%; 
        border-radius: 8px; 
        font-weight: bold; 
        height: 3.5em; 
    }
    </style>
    """, unsafe_allow_html=True)

# --- TELA HOME (CENTRALIZADA) ---
if st.session_state.pagina == "🏠 HOME":
    # Criando 3 colunas para centralizar a imagem na do meio
    col_l, col_c, col_r = st.columns([1, 2, 1])
    
    with col_c:
        if os.path.exists("LOGO.PNG"):
            st.image("LOGO.PNG", use_container_width=True)
        else:
            # Placeholder caso a logo não esteja no diretório
            st.markdown("<h1 style='text-align: center;'>🛡️ ZION TECNOLOGIA</h1>", unsafe_allow_html=True)
            
        st.markdown("<h3 style='text-align: center;'>Gestão Operacional Transdourada</h3>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Botões de Menu
    c1, c2, c3 = st.columns(3)
    if c1.button("📋 NOVO LANÇAMENTO"): st.session_state.dados_edicao = None; navegar("📋 CADASTRO")
    if c2.button("📊 VER AGENDAMENTOS"): navegar("📊 GRADE")
    if c3.button("💰 FINANCEIRO"): navegar("💰 FINANCEIRO")
