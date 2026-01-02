import streamlit as st
import pandas as pd
from fpdf import FPDF
import os
from datetime import datetime
# 1. NOVA IMPORTAÇÃO
from streamlit_gsheets import GSheetsConnection

# CONFIGURAÇÃO E IDENTIDADE VISUAL
st.set_page_config(page_title="ZION TECNOLOGIA", layout="wide")

# 2. CONFIGURAÇÃO DA URL (https://docs.google.com/spreadsheets/d/1Rzm55i-k9PSIc3TUownF4wBiGkQz6IaU-Lruy-dEZQM/edit?usp=sharing)
URL_PLANILHA = "SUA_URL_DA_PLANILHA_AQUI"

# Cria a conexão
conn = st.connection("gsheets", type=GSheetsConnection)

# Função para carregar dados direto da planilha
def carregar_dados():
    try:
        return conn.read(spreadsheet=URL_PLANILHA, ttl="0")
    except:
        return pd.DataFrame(columns=CAMPOS_MESTRES + ["DIAS", "TOTAL", "DT_OBJ"])

# Estilização CSS
st.markdown("""
    <style>
    div.stButton > button:first-child { background-color: #f44336; color: white; border-radius: 5px; height: 3em; font-weight: bold; }
    .st-emotion-cache-19rxjzoef { background-color: #4CAF50 !important; color: white !important; font-weight: bold !important; }
    .stDataFrame { border: 1px solid #f44336; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

CAMPOS_MESTRES = [
    "O.S", "PEDIDO", "CLIENTE", "TIPO", "INICIO", "FIM", "HORA", "SAIDA", 
    "EMPURRADOR", "CMT", "ESCOLTA1", "ESCOLTA2", "LOCAL", "DESTINO", "BALSA", "STATUS", "DESCRIÇÃO", "ASSINATURA"
]

# 3. INICIALIZAÇÃO LENDO A PLANILHA
if 'db_os' not in st.session_state: 
    st.session_state.db_os = carregar_dados()
if 'tela' not in st.session_state: st.session_state.tela = "HOME"
if 'exibir_form' not in st.session_state: st.session_state.exibir_form = False

# ... (Função gerar_pdf_os e Sidebar permanecem iguais) ...

# (Na parte do Botão SALVAR OPERAÇÃO, altere para isso):
            if st.form_submit_button("✅ SALVAR OPERAÇÃO"):
                dias = (fim - ini).days if (fim - ini).days > 0 else 1
                v_dia = 1870.0 if tipo == "ESCOLTA" else 970.0
                
                nova_os = {
                    "O.S": os_n, "PEDIDO": ped, "CLIENTE": cli, "TIPO": tipo, "INICIO": ini.strftime('%d/%m/%Y'),
                    "FIM": fim.strftime('%d/%m/%Y'), "HORA": h_emb, "SAIDA": sai, "EMPURRADOR": emp,
                    "CMT": cmt, "ESCOLTA1": esc1, "ESCOLTA2": esc2, "LOCAL": ori, "DESTINO": dst,
                    "BALSA": bal, "STATUS": "⏳ ANDAMENTO" if stt == "ANDAMENTO" else "✅ ENCERRADO",
                    "DESCRIÇÃO": desc, "ASSINATURA": ass, "DIAS": dias, "TOTAL": dias * v_dia, "DT_OBJ": ini.strftime('%Y-%m-%d')
                }
                
                # Envia para a Planilha
                df_atual = carregar_dados()
                df_novo = pd.concat([df_atual, pd.DataFrame([nova_os])], ignore_index=True)
                conn.update(spreadsheet=URL_PLANILHA, data=df_novo)
                
                st.session_state.db_os = df_novo
                st.session_state.exibir_form = False
                st.success("Salvo no Google Sheets!")
                st.rerun()
