import streamlit as st
import requests
import pandas as pd
import os
import base64

# Configuração da Página
st.set_page_config(page_title="Zion Tecnologia", layout="wide")

# --- CONEXÃO NOTION ---
TOKEN = st.secrets["notion"]["token"].replace('"', '').strip()
DATABASE = st.secrets["notion"]["database_id"].replace('"', '').strip()

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

# --- CONTROLE DE NAVEGAÇÃO ---
if "pagina" not in st.session_state:
    st.session_state.pagina = "🏠 HOME"

def navegar(p):
    st.session_state.pagina = p
    st.rerun()

# Esconde o menu lateral e cabeçalhos do Streamlit para o visual ficar limpo
st.markdown("""
    <style>
        [data-testid="stSidebarNav"] {display: none;}
        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- FUNÇÃO PARA RENDERIZAR LOGO COMO BOTÃO ---
def renderizar_logo_clicavel():
    if os.path.exists("LOGO.PNG"):
        with open("LOGO.PNG", "rb") as f:
            data = base64.b64encode(f.read()).decode("utf-8")
        
        # Criando a imagem centralizada que, ao ser clicada, recarrega a página com um parâmetro
        # Usamos um link fake que o Streamlit captura para mudar o estado
        st.markdown(
            f"""
            <div style="display: flex; justify-content: center; align-items: center; height: 300px;">
                <a href="?acesso=true" target="_self">
                    <img src="data:image/png;base64,{data}" style="width: 450px; cursor: pointer; transition: 0.3s;">
                </a>
            </div>
            """,
            unsafe_allow_html=True
        )

# --- TELA 1: HOME (ABERTURA) ---
if st.session_state.pagina == "🏠 HOME":
    renderizar_logo_clicavel()
    
    # Captura se o usuário clicou na logo através da URL
    params = st.query_params
    if params.get("acesso") == "true":
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📋 NOVO LANÇAMENTO", use_container_width=True, height=100): navegar("📋 AGENDAMENTO")
        with col2:
            if st.button("📊 VER AGENDAMENTO", use_container_width=True, height=100): navegar("📊 VER AGENDAMENTOS")
        with col3:
            if st.button("💰 FINANCEIRO", use_container_width=True, height=100): navegar("💰 FINANCEIRO")

# --- TELA 2: AGENDAMENTO (TODOS OS 17 CAMPOS) ---
elif st.session_state.pagina == "📋 AGENDAMENTO":
    if st.button("🏠 VOLTAR AO INÍCIO"): 
        st.query_params.clear() # Limpa o clique da logo
        navegar("🏠 HOME")
        
    st.header("📋 Cadastro Geral de Missão")
    
    with st.form("form_zion", clear_on_submit=True):
        c1, c2, c3 = st.columns(3)
        # Coluna 1
        os_n = c1.text_input("Nº O.S")
        ini_m = c1.date_input("INÍCIO DA MISSÃO", format="DD/MM/YYYY")
        h_emb = c1.text_input("HORA DE EMBARQUE")
        local = c1.text_input("LOCAL")
        empurrador = c1.text_input("EMPURRADOR")
        
        # Coluna 2
        saida = c2.text_input("SAÍDA")
        fim_m = c2.date_input("FIM DA MISSÃO", format="DD/MM/YYYY")
        esc1 = c2.text_input("ESCOLTA 1")
        esc2 = c2.text_input("ESCOLTA 2")
        servico = c2.selectbox("TIPO DE SERVIÇO", ["Escolta", "Vigilância"])
        
        # Coluna 3
        cliente = c3.text_input("CLIENTE")
        balsa = c3.text_input("BALSA")
        destino = c3.text_input("DESTINO")
        pedido = c3.text_input("Nº PEDIDO")
        assinatura = c3.text_input("ASSINATURA RESPONSÁVEL")
        status = c3.selectbox("STATUS", ["Em Andamento", "Encerrado"])

        desc = st.text_area("DESCRIÇÃO / OBSERVAÇÕES")

        if st.form_submit_button("✅ SALVAR OPERAÇÃO"):
            # Lógica Financeira Zion
            v_servico = 1870.0 if servico == "Escolta" else 970.0
            
            payload = {
                "parent": {"database_id": DATABASE},
                "properties": {
                    "Nº OS": {"title": [{"text": {"content": os_n}}]},
                    "CLIENTE": {"rich_text": [{"text": {"content": cliente}}]},
                    "INÍCIO DA MISSÃO": {"date": {"start": str(ini_m)}},
                    "FIM DA MISSÃO": {"date": {"start": str(fim_m)}},
                    "HORA DE EMBARQUE": {"rich_text": [{"text": {"content": h_emb}}]},
                    "SAÍDA": {"rich_text": [{"text": {"content": saida}}]},
                    "ESCOLTA 1": {"rich_text": [{"text": {"content": esc1}}]},
                    "ESCOLTA 2": {"rich_text": [{"text": {"content": esc2}}]},
                    "LOCAL": {"rich_text": [{"text": {"content": local}}]},
                    "EMPURRADOR": {"rich_text": [{"text": {"content": empurrador}}]},
                    "BALSA": {"rich_text": [{"text": {"content": balsa}}]},
                    "DESTINO": {"rich_text": [{"text": {"content": destino}}]},
                    "PEDIDO": {"rich_text": [{"text": {"content": pedido}}]},
                    "ASSINATURA": {"rich_text": [{"text": {"content": assinatura}}]},
                    "STATUS": {"select": {"name": status}},
                    "SERVIÇO": {"select": {"name": servico}},
                    "VALOR": {"number": v_servico},
                    "DESCRIÇÃO": {"rich_text": [{"text": {"content": desc}}]}
                }
            }
            res = requests.post("https://api.notion.com/v1/pages", headers=headers, json=payload)
            if res.status_code == 200:
                st.success("🎯 Salvo com sucesso! Redirecionando...")
                navegar("📊 VER AGENDAMENTOS")
            else:
                st.error(f"Erro: {res.text}")

# --- TELA 3: VER AGENDAMENTOS (TABELA COM PDF E EDIÇÃO) ---
elif st.session_state.pagina == "📊 VER AGENDAMENTOS":
    if st.button("🏠 VOLTAR AO INÍCIO"): 
        st.query_params.clear()
        navegar("🏠 HOME")
        
    st.header("📊 Operações Realizadas")
    # Busca de dados igual ao vídeo, com botões por linha
    # ... (lógica de buscar_dados)
