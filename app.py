import streamlit as st
import pandas as pd

# 1. CONFIGURAÇÃO DA PÁGINA (Sempre a primeira linha)
st.set_page_config(page_title="Zion Tecnologia", layout="centered")

# 2. CSS SEGURO (Embutido para não dar SyntaxError)
st.markdown("""
    <style>
    /* Estilização dos botões */
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        height: 3.5em;
        background-color: white;
        border: 1px solid #cccccc;
        font-weight: bold;
    }
    /* Efeito na Logo */
    [data-testid="stImage"] {
        cursor: pointer;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. LÓGICA DE NAVEGAÇÃO
if 'pagina' not in st.session_state:
    st.session_state.pagina = 'inicio'

def mudar_pagina(nome):
    st.session_state.pagina = nome

# --- ÁREA SUPERIOR ---
col_vazia, col_btn = st.columns([3, 1])
with col_btn:
    if st.button("☰ OPERACIONAL"):
        mudar_pagina('menu')

# --- TELA DE MENU (ÍCONES) ---
if st.session_state.pagina == 'menu':
    st.title("⚙️ Painel Operacional")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📋 NOVO LANÇAMENTO"):
            mudar_pagina('cadastro')
    with col2:
        if st.button("📊 AGENDAMENTOS"):
            mudar_pagina('inicio')
    with col3:
        if st.button("💰 FINANCEIRO"):
            st.info("Módulo Financeiro em breve.")
            
    if st.button("← VOLTAR PARA O INÍCIO"):
        mudar_pagina('inicio')

# --- TELA DE CADASTRO (ONDE ESTAVA O ERRO DO BANCO) ---
elif st.session_state.pagina == 'cadastro':
    st.subheader("📝 Cadastrar Operação")
    
    nome = st.text_input("Nome do Cliente")
    servico = st.selectbox("Serviço", ["Vigilância", "Monitoramento", "Escolta"])
    # AQUI ESTAVA O PROBLEMA: Verifique se o banco espera 'valor' ou 'preço'
    valor_input = st.number_input("Valor da Operação", min_value=0.0)

    if st.button("✅ SALVAR OPERAÇÃO EM LINHA ÚNICA"):
        try:
            # CORREÇÃO DO ERRO 400: 
            # O nome da chave deve ser EXATAMENTE igual ao nome da coluna no seu Banco
            dados = {
                "cliente": nome,
                "servico": servico,
                "valor": valor_input  # Mudei de "VALOR" para "valor" (minúsculo)
            }
            
            # COMANDO DE INSERÇÃO (Exemplo genérico - ajuste para sua conexão)
            # res = supabase.table("sua_tabela").insert(dados).execute()
            st.success("Operação salva com sucesso!")
            
        except Exception as e:
            st.error(f"Erro de Validação: Verifique se a coluna no banco se chama 'valor' ou 'VALOR'.")
            st.code(str(e))

# --- TELA DE INÍCIO (LOGO E TABELA) ---
else:
    # Exibição da Logo
    try:
        # Substitua 'logo.png' pelo seu arquivo local ou URL
        st.image("logo.png", use_container_width=True)
    except:
        st.markdown("<h1 style='text-align: center;'>ZION TECNOLOGIA</h1>", unsafe_allow_html=True)

    st.markdown("---")
    
    # Grade de Agendamentos (Tabela)
    st.subheader("📅 Agendamentos do Dia")
    
    # Criando uma tabela visual com bordas
    df_exemplo = pd.DataFrame(
        columns=["HORÁRIO", "CLIENTE", "SERVIÇO", "STATUS"]
    )
    
    if df_exemplo.empty:
        st.warning("Nenhum agendamento encontrado para hoje.")
        # Forçando a exibição das colunas mesmo vazias
        st.table(pd.DataFrame(columns=["HORÁRIO", "CLIENTE", "SERVIÇO", "STATUS"]))
    else:
        st.table(df_exemplo)
