import streamlit as st
import requests
import pandas as pd
import os
from fpdf import FPDF
from datetime import datetime

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Zion Tecnologia - Gestão Transdourada", layout="wide")

# --- CONEXÃO NOTION (SEGURANÇA TOTAL) ---
try:
    TOKEN = st.secrets["notion"]["token"].replace('"', '').strip()
    DATABASE = st.secrets["notion"]["database_id"].replace('"', '').strip()
except Exception as e:
    st.error("Erro nos Secrets: Verifique se 'token' e 'database_id' estão configurados.")
    st.stop()

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

# --- ESTILO CSS ---
st.markdown("""
    <style>
    div.stButton > button:first-child[kind="primary"] { background-color: #28a745 !important; color: white !important; }
    .stButton>button { width: 100%; border-radius: 8px; font-weight: bold; height: 3.5em; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNÇÃO CARREGAR DADOS (REVISADA E BLINDADA) ---
def carregar_dados_notion():
    try:
        res = requests.post(f"https://api.notion.com/v1/databases/{DATABASE}/query", headers=headers)
        if res.status_code == 200:
            results = res.json().get("results", [])
            lista = []
            for r in results:
                p = r["properties"]
                
                # Função interna para capturar dados sem quebrar o código
                def g_t(n): 
                    try: return p[n]["rich_text"][0]["plain_text"] if p[n]["rich_text"] else "---"
                    except: return "---"
                def g_d(n): 
                    try: return datetime.strptime(p[n]["date"]["start"], '%Y-%m-%d').strftime('%d/%m/%Y') if p[n]["date"] else "---"
                    except: return "---"
                def g_s(n):
                    try: return p[n]["select"]["name"] if p[n]["select"] else "---"
                    except: return "---"
                def g_title():
                    try: return p["Nº OS"]["title"][0]["plain_text"] if p["Nº OS"]["title"] else "---"
                    except: return "---"

                lista.append({
                    "ID": r["id"],
                    "Nº OS": g_title(),
                    "CLIENTE": g_t("CLIENTE"), 
                    "DT SAÍDA": g_d("DT SAÍDA"),
                    "EMPURRADOR": g_t("EMPURRADOR"), 
                    "BALSA": g_t("BALSA"),
                    "LOCAL": g_t("LOCAL"), 
                    "DESTINO": g_t("DESTINO"),
                    "HORA_EMBARQUE": g_t("HORA DE EMBARQUE"),
                    "ESCOLTA 1": g_t("ESCOLTA 1"), 
                    "ESCOLTA 2": g_t("ESCOLTA 2"),
                    "DESCRIÇÃO": g_t("DESCRIÇÃO"), 
                    "PEDIDO": g_t("PEDIDO"),
                    "INÍCIO": g_d("INÍCIO DA MISSÃO"), 
                    "FIM": g_d("FIM DA MISSÃO"),
                    "ASSINATURA": g_t("ASSINATURA RESPONSÁVEL"),
                    "STATUS": g_s("STATUS")
                })
            return lista
        return []
    except:
        return []

# --- FUNÇÃO GERAR PDF ---
def gerar_pdf_os(d):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "TRANSDOURADA NAVEGAÇÃO LTDA - ORDEM DE SERVIÇO", ln=True, align="C")
    pdf.ln(5)
    pdf.set_font("Arial", "B", 10)
    pdf.cell(0, 8, f"O.S Nº: {d['Nº OS']} | STATUS: {d['STATUS']}", border=1, ln=True)
    pdf.cell(0, 8, f"CLIENTE: {d['CLIENTE']}", border=1, ln=True)
    pdf.cell(95, 8, f"EMPURRADOR: {d['EMPURRADOR']}", border=1)
    pdf.cell(95, 8, f"BALSA: {d['BALSA']}", border=1, ln=True)
    pdf.ln(5)
    pdf.multi_cell(0, 6, f"DESCRIÇÃO: {d['DESCRIÇÃO']}", border=1)
    return pdf.output(dest="S").encode("latin-1")

# --- NAVEGAÇÃO ---
if "pagina" not in st.session_state: st.session_state.pagina = "🏠 HOME"
if "dados_edicao" not in st.session_state: st.session_state.dados_edicao = None
def navegar(p): st.session_state.pagina = p; st.rerun()

# --- TELAS ---
if st.session_state.pagina == "🏠 HOME":
    if os.path.exists("LOGO.PNG"): st.image("LOGO.PNG", width=200)
    st.title("🛡️ Sistema Zion Tecnologia")
    c1, c2, c3 = st.columns(3)
    if c1.button("📋 NOVO LANÇAMENTO"): st.session_state.dados_edicao = None; navegar("📋 CADASTRO")
    if c2.button("📊 VER AGENDAMENTOS"): navegar("📊 GRADE")
    if c3.button("💰 FINANCEIRO"): navegar("💰 FINANCEIRO")

elif st.session_state.pagina == "📋 CADASTRO":
    edit = st.session_state.dados_edicao
    st.header("📝 Formulário de O.S")
    if st.button("⬅️ VOLTAR"): navegar("🏠 HOME")
    
    with st.form("form_os"):
        c1, c2, c3 = st.columns(3)
        os_n = c1.text_input("Nº O.S", value=edit["Nº OS"] if edit else "")
        dt_s = c2.date_input("DATA SAÍDA")
        cli = c3.text_input("CLIENTE", value=edit["CLIENTE"] if edit else "")
        
        c4, c5, c6 = st.columns(3)
        emp = c4.text_input("EMPURRADOR", value=edit["EMPURRADOR"] if edit else "")
        bal = c5.text_input("BALSA", value=edit["BALSA"] if edit else "")
        h_e = c6.text_input("HORA EMBARQUE", value=edit.get("HORA_EMBARQUE", "") if edit else "")
        
        obs = st.text_area("DESCRIÇÃO", value=edit.get("DESCRIÇÃO", "") if edit else "")
        sts = st.selectbox("STATUS", ["Em Andamento", "Encerrado"])
        
        if st.form_submit_button("✅ SALVAR OPERAÇÃO", type="primary"):
            payload = {"properties": {
                "Nº OS": {"title": [{"text": {"content": str(os_n)}}]},
                "CLIENTE": {"rich_text": [{"text": {"content": cli}}]},
                "DT SAÍDA": {"date": {"start": dt_s.strftime('%Y-%m-%d')}},
                "EMPURRADOR": {"rich_text": [{"text": {"content": emp}}]},
                "BALSA": {"rich_text": [{"text": {"content": bal}}]},
                "HORA de EMBARQUE": {"rich_text": [{"text": {"content": h_e}}]},
                "DESCRIÇÃO": {"rich_text": [{"text": {"content": obs}}]},
                "STATUS": {"select": {"name": sts}}
            }}
            
            url = f"https://api.notion.com/v1/pages/{edit['ID']}" if edit else "https://api.notion.com/v1/pages"
            if not edit: payload["parent"] = {"database_id": DATABASE}
            
            res = requests.patch(url, headers=headers, json=payload) if edit else requests.post(url, headers=headers, json=payload)
            
            if res.status_code == 200:
                st.success("🎯 Salvo com sucesso!"); navegar("📊 GRADE")
            else:
                st.error(f"Erro ao salvar: {res.json().get('message', 'Verifique os nomes das colunas no Notion')}")

elif st.session_state.pagina == "📊 GRADE":
    st.header("📊 Agendamentos Ativos")
    if st.button("⬅️ HOME"): navegar("🏠 HOME")
    dados = carregar_dados_notion()
    if dados:
        df = pd.DataFrame(dados)
        st.dataframe(df[["Nº OS", "CLIENTE", "DT SAÍDA", "STATUS"]], use_container_width=True)
        for d in dados:
            with st.expander(f"O.S {d['Nº OS']} - {d['CLIENTE']}"):
                c1, c2 = st.columns(2)
                if c1.button("✏️ EDITAR", key=f"ed_{d['ID']}"):
                    st.session_state.dados_edicao = d; navegar("📋 CADASTRO")
                pdf = gerar_pdf_os(d)
                c2.download_button("📄 PDF", pdf, f"OS_{d['Nº OS']}.pdf", key=f"p_{d['ID']}")
    else:
        st.info("Nenhum dado encontrado no Notion.")

elif st.session_state.pagina == "💰 FINANCEIRO":
    st.header("💰 Resumo Financeiro")
    if st.button("⬅️ VOLTAR"): navegar("🏠 HOME")
    dados = carregar_dados_notion()
    if dados:
        df = pd.DataFrame(dados)
        st.table(df[["Nº OS", "CLIENTE", "DT SAÍDA", "STATUS"]])
    else:
        st.info("Sem dados para exibir.")
