import streamlit as st
import requests
import pandas as pd
import os
import base64

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Zion Tecnologia", layout="wide")

# --- CONEXÃO NOTION ---
TOKEN = st.secrets["notion"]["token"].replace('"', '').strip()
DATABASE = st.secrets["notion"]["database_id"].replace('"', '').strip()

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

# --- CSS PARA GRADE E DESIGN (PROTEGIDO) ---
st.markdown("""
    <style>
    .grade-zion {
        width: 100%;
        border-collapse: collapse;
        background-color: white;
        color: black;
    }
    .grade-zion th {
        border: 2px solid #000000 !important;
        background-color: #f0f2f6;
        padding: 12px;
        text-align: left;
        font-weight: bold;
    }
    .grade-zion td {
        border: 2px solid #000000 !important;
        padding: 10px;
    }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# --- CONTROLE DE ESTADO ---
if "mostrar_icones" not in st.session_state:
    st.session_state.mostrar_icones = False
if "pagina" not in st.session_state:
    st.session_state.pagina = "🏠 HOME"

def navegar(p):
    st.session_state.pagina = p
    st.rerun()

# --- BOTÃO AUXILIAR NO TOPO ---
col_logo_top, col_auxiliar = st.columns([5, 1])
with col_auxiliar:
    if st.button("☰ OPERACIONAL"):
        st.session_state.mostrar_icones = True
        navegar("🏠 HOME")

# --- FUNÇÃO LOGO ---
def logo_central():
    if os.path.exists("LOGO.PNG"):
        with open("LOGO.PNG", "rb") as f:
            data = base64.b64encode(f.read()).decode("utf-8")
        st.markdown(
            f"""
            <div style="display: flex; justify-content: center; margin-bottom: 20px;">
                <img src="data:image/png;base64,{data}" style="width: 450px;">
            </div>
            """,
            unsafe_allow_html=True
        )

# --- NAVEGAÇÃO DE TELAS ---

if st.session_state.pagina == "🏠 HOME":
    logo_central()
    
    if not st.session_state.mostrar_icones:
        if st.button("🔓 ACESSAR ÍCONES OPERACIONAIS"):
            st.session_state.mostrar_icones = True
            st.rerun()

    if st.session_state.mostrar_icones:
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("📋 NOVO LANÇAMENTO"): navegar("📋 AGENDAMENTO")
        with c2:
            if st.button("📊 VER AGENDAMENTO"): navegar("📊 VER AGENDAMENTOS")
        with c3:
            if st.button("💰 FINANCEIRO"): navegar("💰 FINANCEIRO")
    
    st.markdown("---")
    st.subheader("📅 Grade de Agendamentos")
    
    # GRADE ATUALIZADA COM COLUNA "DT SAÍDA"
    st.markdown("""
        <table class="grade-zion">
            <thead>
                <tr>
                    <th>HORÁRIO</th>
                    <th>CLIENTE</th>
                    <th>SERVIÇO</th>
                    <th>DT SAÍDA</th>
                    <th>STATUS</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td colspan="5" style="text-align:center; padding: 30px; color: gray;">
                        Aguardando integração de dados... (Coluna DT SAÍDA ativa)
                    </td>
                </tr>
            </tbody>
        </table>
        """, unsafe_allow_html=True)

elif st.session_state.pagina == "📋 AGENDAMENTO":
    if st.button("⬅️ VOLTAR"):
        st.session_state.mostrar_icones = True
        navegar("🏠 HOME")
        
    st.header("📋 Cadastro Geral de Missão")
    
    with st.form("form_completo"):
        c1, c2, c3 = st.columns(3)
        # Coluna 1
        os_n = c1.text_input("Nº O.S")
        ini_m = c1.date_input("INÍCIO DA MISSÃO", format="DD/MM/YYYY")
        h_emb = c1.text_input("HORA DE EMBARQUE")
        local = c1.text_input("LOCAL")
        empurrador = c1.text_input("EMPURRADOR")
        
        # Coluna 2 (Ajustada)
        dt_saida_val = c2.text_input("DT SAÍDA") # Nome ajustado aqui
        fim_m = c2.date_input("FIM DA MISSÃO", format="DD/MM/YYYY")
        esc1 = c2.text_input("ESCOLTA 1")
        esc2 = c2.text_input("ESCOLTA 2")
        servico = c2.selectbox("SERVIÇO", ["Escolta", "Vigilância"])
        
        # Coluna 3
        cliente = c3.text_input("CLIENTE")
        balsa = c3.text_input("BALSA")
        destino = c3.text_input("DESTINO")
        pedido = c3.text_input("PEDIDO")
        assinatura = c3.text_input("ASSINATURA RESPONSÁVEL")
        status = c3.selectbox("STATUS", ["Em Andamento", "Encerrado"])

        desc = st.text_area("DESCRIÇÃO / OBSERVAÇÕES")

        if st.form_submit_button("✅ SALVAR OPERAÇÃO EM LINHA ÚNICA"):
            valor_fin = 1870.0 if servico == "Escolta" else 970.0
            
            payload = {
                "parent": {"database_id": DATABASE},
                "properties": {
                    "Nº OS": {"title": [{"text": {"content": os_n}}]},
                    "CLIENTE": {"rich_text": [{"text": {"content": cliente}}]},
                    "INÍCIO DA MISSÃO": {"date": {"start": str(ini_m)}},
                    "FIM DA MISSÃO": {"date": {"start": str(fim_m)}},
                    "HORA DE EMBARQUE": {"rich_text": [{"text": {"content": h_emb}}]},
                    "DT SAÍDA": {"rich_text": [{"text": {"content": dt_saida_val}}]}, # PROPRIEDADE AJUSTADA
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
                st.success("🎯 Salvo com sucesso no Notion!")
                navegar("🏠 HOME")
            else:
                st.error(f"Erro de Propriedade: Verifique se no Notion a coluna se chama exatamente 'DT SAÍDA'.")
                st.code(res.text)

elif st.session_state.pagina == "📊 VER AGENDAMENTOS":
    if st.button("⬅️ VOLTAR"): navegar("🏠 HOME")
    st.title("📊 Relatório de Agendamentos")
