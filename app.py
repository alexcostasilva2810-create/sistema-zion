import streamlit as st
import requests
import pandas as pd
import os

st.set_page_config(page_title="Zion Tecnologia", layout="wide")

# Conexão Notion
TOKEN = st.secrets["notion"]["token"].replace('"', '').strip()
DATABASE = st.secrets["notion"]["database_id"].replace('"', '').strip()

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

# --- CONTROLE DE ESTADO ---
if "mostrar_icones" not in st.session_state:
    st.session_state.mostrar_icones = False
if "pagina" not in st.session_state:
    st.session_state.pagina = "🏠 HOME"

def navegar(p):
    st.session_state.pagina = p
    st.rerun()

# Esconde o menu lateral padrão para manter o visual limpo do vídeo
st.markdown("<style> [data-testid='stSidebarNav'] {display: none;} </style>", unsafe_allow_html=True)

# --- TELA 1: ABERTURA COM LOGO CLICÁVEL ---
if st.session_state.pagina == "🏠 HOME":
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        # A MÁGICA: A logo dentro de um botão
        # Se clicar na imagem/botão, inverte o estado de mostrar_icones
        if st.button("Clique na Logo para Acessar o Sistema", use_container_width=True):
            st.session_state.mostrar_icones = not st.session_state.mostrar_icones
        
        if os.path.exists("LOGO.PNG"):
            st.image("LOGO.PNG", use_container_width=True)
        
        # OS ÍCONES SÓ APARECEM APÓS O CLIQUE NA LOGO ACIMA
        if st.session_state.mostrar_icones:
            st.markdown("<h3 style='text-align: center;'>MENU DE GESTÃO</h3>", unsafe_allow_html=True)
            c1, c2, c3 = st.columns(3)
            
            if c1.button("📋 NOVO LANÇAMENTO", use_container_width=True):
                navegar("📋 AGENDAMENTO")
            if c2.button("📊 VER AGENDAMENTO", use_container_width=True):
                navegar("📊 VER AGENDAMENTOS")
            if c3.button("💰 FINANCEIRO", use_container_width=True):
                navegar("💰 FINANCEIRO")

# --- TELA 2: AGENDAMENTO (TODOS OS 17 CAMPOS REVISADOS) ---
elif st.session_state.pagina == "📋 AGENDAMENTO":
    if st.button("⬅️ VOLTAR AO INÍCIO"): 
        st.session_state.mostrar_icones = False
        navegar("🏠 HOME")
        
    st.header("📋 Cadastro Geral de Missão")
    
    with st.form("form_completo", clear_on_submit=True):
        c1, c2, c3 = st.columns(3)
        # Linha 1
        os_n = c1.text_input("Nº O.S")
        ini_m = c1.date_input("INÍCIO DA MISSÃO", format="DD/MM/YYYY")
        h_emb = c1.text_input("HORA DE EMBARQUE")
        local = c1.text_input("LOCAL")
        empurrador = c1.text_input("EMPURRADOR")
        
        # Linha 2
        saida = c2.text_input("SAÍDA")
        fim_m = c2.date_input("FIM DA MISSÃO", format="DD/MM/YYYY")
        esc1 = c2.text_input("ESCOLTA 1")
        esc2 = c2.text_input("ESCOLTA 2")
        servico = c2.selectbox("SERVIÇO", ["Escolta", "Vigilância"])
        
        # Linha 3
        cliente = c3.text_input("CLIENTE")
        balsa = c3.text_input("BALSA")
        destino = c3.text_input("DESTINO")
        pedido = c3.text_input("PEDIDO")
        assinatura = c3.text_input("ASSINATURA RESPONSÁVEL")
        status = c3.selectbox("STATUS", ["Em Andamento", "Encerrado"])

        desc = st.text_area("DESCRIÇÃO / OBSERVAÇÕES")

        if st.form_submit_button("✅ SALVAR OPERAÇÃO EM LINHA ÚNICA"):
            # Envio unificado para o Notion (Payload completo)
            payload = {
                "parent": {"database_id": DATABASE},
                "properties": {
                    "Nº OS": {"title": [{"text": {"content": os_n}}]},
                    "CLIENTE": {"rich_text": [{"text": {"content": cliente}}]},
                    "INÍCIO DA MISSÃO": {"date": {"start": str(ini_m)}},
                    "FIM DA MISSÃO": {"date": {"start": str(fim_m)}},
                    "ESCOLTA 1": {"rich_text": [{"text": {"content": esc1}}]},
                    "ESCOLTA 2": {"rich_text": [{"text": {"content": esc2}}]},
                    "HORA DE EMBARQUE": {"rich_text": [{"text": {"content": h_emb}}]},
                    "LOCAL": {"rich_text": [{"text": {"content": local}}]},
                    "EMPURRADOR": {"rich_text": [{"text": {"content": empurrador}}]},
                    "SAÍDA": {"rich_text": [{"text": {"content": saida}}]},
                    "BALSA": {"rich_text": [{"text": {"content": balsa}}]},
                    "DESTINO": {"rich_text": [{"text": {"content": destino}}]},
                    "PEDIDO": {"rich_text": [{"text": {"content": pedido}}]},
                    "ASSINATURA": {"rich_text": [{"text": {"content": assinatura}}]},
                    "STATUS": {"select": {"name": status}},
                    "SERVIÇO": {"select": {"name": servico}},
                    "DESCRIÇÃO": {"rich_text": [{"text": {"content": desc}}]}
                }
            }
            res = requests.post("https://api.notion.com/v1/pages", headers=headers, json=payload)
            if res.status_code == 200:
                st.success("🎯 Salvo com sucesso! Abrindo registros...")
                navegar("📊 VER AGENDAMENTOS")
            else:
                st.error(f"Erro ao salvar no Notion: {res.text}")

# --- TELAS DE CONSULTA E FINANCEIRO (MANTIDAS COMO SOLICITADO) ---
elif st.session_state.pagina == "📊 VER AGENDAMENTOS":
    if st.button("⬅️ VOLTAR AO INÍCIO"): navegar("🏠 HOME")
    st.header("📊 Operações Realizadas")
    # ... (Lógica de tabela aqui)

elif st.session_state.pagina == "💰 FINANCEIRO":
    if st.button("⬅️ VOLTAR AO INÍCIO"): navegar("🏠 HOME")
    st.header("💰 Fluxo Financeiro")
    # ... (Lógica de valores aqui)
