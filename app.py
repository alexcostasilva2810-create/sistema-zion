import streamlit as st

# 1. Configuração da Página
st.set_page_config(layout="wide")

# 2. CSS para Logo Clicável e Tabela com Colunas Visíveis
st.markdown("""
    <style>
    /* Estilo da Logo Clicável */
    .logo-container {
        display: flex;
        justify-content: center;
        cursor: pointer;
        padding: 20px;
        transition: 0.3s;
    }
    .logo-container:hover { transform: scale(1.02); }
    
    /* Estilo da Tabela com Bordas Pretas (Grade Visível) */
    .tabela-zion {
        width: 100%;
        border-collapse: collapse;
        margin-top: 20px;
    }
    .tabela-zion th, .tabela-zion td {
        border: 2px solid #000000 !important;
        padding: 12px;
        text-align: left;
    }
    .tabela-zion th {
        background-color: #f0f2f6;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Lógica de Navegação
if 'pagina' not in st.session_state:
    st.session_state.pagina = 'tabela'

def navegar(nome_pagina):
    st.session_state.pagina = nome_pagina

# --- BOTÃO AUXILIAR NO TOPO ---
col_logo, col_btn = st.columns([4, 1])

with col_btn:
    if st.button("☰ ÍCONES OPERACIONAIS", use_container_width=True):
        navegar('menu')

# --- TELA DE ÍCONES (MENU) ---
if st.session_state.pagina == 'menu':
    st.title("⚙️ Operacional")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📅 NOVO LANÇAMENTO", use_container_width=True, height=100):
            st.info("Abrindo Novo Lançamento...")
    with col2:
        if st.button("📊 VER AGENDAMENTOS", use_container_width=True, height=100):
            navegar('tabela')
    with col3:
        if st.button("💰 FINANCEIRO", use_container_width=True, height=100):
            st.info("Abrindo Financeiro...")
            
    if st.button("← Voltar para Início"):
        navegar('tabela')

# --- TELA DA TABELA (PRINCIPAL) ---
else:
    # LOGO CLICÁVEL (A imagem do seu sistema)
    # Substitua o link abaixo pelo caminho da sua imagem ou URL
    logo_url = "https://raw.githubusercontent.com/SeuUsuario/SeuRepo/main/logo.png" 
    
    st.markdown(f"""
        <div class="logo-container" onclick="window.location.href='#menu'">
            <img src="{logo_url}" width="400">
        </div>
        """, unsafe_allow_html=True)
    
    st.subheader("📋 Grade de Agendamentos")
    
    # Renderização da Tabela Manual para garantir as colunas
    st.markdown("""
        <table class="tabela-zion">
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
                    <td colspan="4" style="text-align:center; padding: 30px; color: gray;">
                        Nenhum agendamento encontrado. As colunas estão ativas.
                    </td>
                </tr>
            </tbody>
        </table>
        """, unsafe_allow_html=True)
