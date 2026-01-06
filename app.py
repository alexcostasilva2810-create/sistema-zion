import streamlit as st
import requests
from fpdf import FPDF
import os

st.set_page_config(page_title="Zion Tecnologia - Gestão", layout="wide")

# Conexão Notion
TOKEN = st.secrets["notion"]["token"].replace('"', '').strip()
DATABASE = st.secrets["notion"]["database_id"].replace('"', '').strip()

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

def mostrar_logo(largura=200):
    if os.path.exists("LOGO.PNG"):
        st.image("LOGO.PNG", width=largura)
    else:
        st.title("🛡️ ZION TECNOLOGIA")

# --- MENU LATERAL ---
with st.sidebar:
    mostrar_logo(150)
    st.markdown("---")
    menu = st.radio("NAVEGAÇÃO", ["🏠 HOME", "📋 AGENDAMENTO ZION", "💰 FINANCEIRO", "🖨️ GERAR PDF"])

# --- TELA 1: HOME ---
if menu == "🏠 HOME":
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        mostrar_logo(450)
        st.markdown("<h2 style='text-align: center;'>BEM-VINDO AO APP GESTÃO DE ESCOLTA</h2>", unsafe_allow_html=True)

# --- TELA 2: AGENDAMENTO (TODOS OS CAMPOS MENOS CMT) ---
elif menu == "📋 AGENDAMENTO ZION":
    st.header("📋 Novo Registro de Operação")
    with st.form("form_completo", clear_on_submit=True):
        c1, c2, c3 = st.columns(3)
        
        # Coluna 1
        os_val = c1.text_input("Nº OS")
        ini_missao = c1.date_input("DATA INÍCIO")
        hora_emb = c1.text_input("HORA EMBARQUE")
        local = c1.text_input("LOCAL")
        
        # Coluna 2
        empurrador = c2.text_input("EMPURRADOR")
        saida = c2.text_input("SAÍDA")
        fim_missao = c2.date_input("DATA FIM")
        esc1 = c2.text_input("ESCOLTA 1")
        
        # Coluna 3
        esc2 = c3.text_input("ESCOLTA 2")
        cliente = c3.text_input("CLIENTE")
        balsa = c3.text_input("BALSA")
        destino = c3.text_input("DESTINO")
        
        # Campos de largura total
        pedido = st.text_input("PEDIDO")
        assinatura = st.text_input("ASSINATURA")
        desc = st.text_area("DESCRIÇÃO")

        if st.form_submit_button("✅ SALVAR OPERAÇÃO"):
            # PAYLOAD: Comunicação com o Notion
            payload = {
                "parent": {"database_id": DATABASE},
                "properties": {
                    "Nº OS": {"title": [{"text": {"content": os_val}}]},
                    "CLIENTE": {"rich_text": [{"text": {"content": cliente}}]},
                    "DATA INÍCIO": {"date": {"start": str(ini_missao)}},
                    "HORA EMBARQUE": {"rich_text": [{"text": {"content": hora_emb}}]},
                    "LOCAL": {"rich_text": [{"text": {"content": local}}]},
                    "EMPURRADOR": {"rich_text": [{"text": {"content": empurrador}}]},
                    "SAÍDA": {"rich_text": [{"text": {"content": saida}}]},
                    "DATA FIM": {"date": {"start": str(fim_missao)}},
                    "ESCOLTA 1": {"rich_text": [{"text": {"content": esc1}}]},
                    "ESCOLTA 2": {"rich_text": [{"text": {"content": esc2}}]},
                    "BALSA": {"rich_text": [{"text": {"content": balsa}}]},
                    "DESTINO": {"rich_text": [{"text": {"content": destino}}]},
                    "PEDIDO": {"rich_text": [{"text": {"content": pedido}}]},
                    "ASSINATURA": {"rich_text": [{"text": {"content": assinatura}}]},
                    "DESCRIÇÃO": {"rich_text": [{"text": {"content": desc}}]}
                }
            }
            res = requests.post("https://api.notion.com/v1/pages", headers=headers, json=payload)
            if res.status_code == 200:
                st.success("🎯 AGORA FOI! Verifique sua tabela no Notion.")
            else:
                st.error(f"Erro de Validação: {res.text}")

# --- TELAS ADICIONAIS ---
elif menu == "💰 FINANCEIRO":
    st.title("💰 Financeiro")
elif menu == "🖨️ GERAR PDF":
    st.title("🖨️ Gerador de Documentos")
