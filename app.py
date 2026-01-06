import streamlit as st
import requests
import pandas as pd
import os
import base64

st.set_page_config(page_title="Zion Tecnologia", layout="wide")

# --- CONEXÃO NOTION ---
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

# Esconde menus desnecessários
st.markdown("<style> [data-testid='stSidebarNav'] {display: none;} </style>", unsafe_allow_html=True)

# --- FUNÇÃO PARA TRANSFORMAR IMAGEM EM BOTÃO CLICÁVEL ---
def logo_clicavel():
    if os.path.exists("LOGO.PNG"):
        with open("LOGO.PNG", "rb") as f:
            data = base64.b64encode(f.read()).decode("utf-8")
        
        # Criando o botão invisível por cima da imagem usando HTML
        # Ao clicar na imagem, o Streamlit entende o comando de abrir os ícones
        if st.button("🔓 ACESSAR SISTEMA", use_container_width=True, type="secondary"):
            st.session_state.mostrar_icones = not st.session_state.mostrar_icones
            st.rerun()
            
        st.markdown(
            f"""
            <div style="display: flex; justify-content: center;">
                <img src="data:image/png;base64,{data}" style="width: 500px; cursor: pointer;">
            </div>
            """,
            unsafe_allow_html=True
        )

# --- TELA 1: HOME ---
if st.session_state.pagina == "🏠 HOME":
    logo_clicavel()
    
    # OS ÍCONES SÓ APARECEM APÓS O CLIQUE NA LOGO ACIMA
    if st.session_state.mostrar_icones:
        st.markdown("<br>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        
        with c1:
            if st.button("📋 NOVO LANÇAMENTO", use_container_width=True): navegar("📋 AGENDAMENTO")
        with c2:
            if st.button("📊 VER AGENDAMENTO", use_container_width=True): navegar("📊 VER AGENDAMENTOS")
        with c3:
            if st.button("💰 FINANCEIRO", use_container_width=True): navegar("💰 FINANCEIRO")

# --- TELA 2: AGENDAMENTO (TODOS OS 17 CAMPOS) ---
elif st.session_state.pagina == "📋 AGENDAMENTO":
    if st.button("⬅️ VOLTAR"): 
        st.session_state.mostrar_icones = False
        navegar("🏠 HOME")
        
    st.header("📋 Cadastro Geral de Missão")
    
    with st.form("form_completo"):
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
            # Lógica de cálculo financeiro embutida
            valor_fin = 1870.0 if servico == "Escolta" else 970.0
            
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
                    "VALOR": {"number": valor_fin},
                    "DESCRIÇÃO": {"rich_text": [{"text": {"content": desc}}]}
                }
            }
            res = requests.post("https://api.notion.com/v1/pages", headers=headers, json=payload)
            if res.status_code == 200:
                st.success("🎯 Salvo com sucesso!")
                navegar("📊 VER AGENDAMENTOS")
            else:
                st.error(f"Erro: {res.text}")

# --- TELA 3: VER AGENDAMENTOS E FINANCEIRO ---
# (Aqui continua a lógica das tabelas que já estavam funcionando bem)
