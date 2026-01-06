import streamlit as st
import requests
import pandas as pd
import os
from fpdf import FPDF
from datetime import datetime

# 1. CONFIGURAÇÃO DA PÁGINA (CONGELADA)
st.set_page_config(page_title="Zion Tecnologia", layout="wide")

# --- CONEXÃO NOTION ---
TOKEN = st.secrets["notion"]["token"].replace('"', '').strip()
DATABASE = st.secrets["notion"]["database_id"].replace('"', '').strip()

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

# --- ESTILO CSS (BOTÃO VERDE) ---
st.markdown("""
    <style>
    div.stButton > button:first-child[kind="primary"] { background-color: #28a745 !important; color: white !important; border: none; }
    .stButton>button { width: 100%; border-radius: 8px; font-weight: bold; height: 3.5em; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNÇÃO GERAR PDF (CONGELADA) ---
def gerar_pdf_transdourada(d):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 10); pdf.cell(0, 5, "ZION TECNOLOGIA | TRANSDOURADA", ln=True)
    pdf.set_font("Arial", "B", 16); pdf.cell(0, 10, "Solicitação de Escolta", ln=True, align="C")
    pdf.cell(0, 7, f"O.S: {d.get('Nº OS', '---')}", ln=True, align="C")
    pdf.ln(5); pdf.cell(0, 10, f"SOLICITANTE ( {d.get('CLIENTE', '---').upper()} )", border=1, ln=True, align="C")
    pdf.ln(5); pdf.set_font("Arial", "", 10)
    pdf.multi_cell(0, 6, f"EMPURRADOR: {d.get('EMPURRADOR', '---')}\nBALSA: {d.get('BALSA', '---')}\nDESCRIÇÃO: {d.get('DESCRIÇÃO', '---')}")
    pdf.set_y(-30); pdf.set_font("Arial", "", 7); pdf.cell(0, 4, "TRANSDOURADA NAVEGAÇÃO LTDA - ANANINDEUA/PA", ln=True, align="C")
    return pdf.output(dest="S").encode("latin-1")

# --- FUNÇÃO CARREGAR DADOS ---
def carregar_dados_notion():
    try:
        res = requests.post(f"https://api.notion.com/v1/databases/{DATABASE}/query", headers=headers)
        if res.status_code == 200:
            results = res.json().get("results", [])
            lista = []
            for r in results:
                p = r["properties"]
                def g_t(n): return p[n]["rich_text"][0]["plain_text"] if n in p and p[n]["rich_text"] else "---"
                def g_d(n): return p[n]["date"]["start"] if n in p and p[n]["date"] else "---"
                lista.append({
                    "ID": r["id"],
                    "Nº OS": p["Nº OS"]["title"][0]["plain_text"] if p["Nº OS"]["title"] else "---",
                    "CLIENTE": g_t("CLIENTE"), "DT SAÍDA": g_d("DT SAÍDA"),
                    "EMPURRADOR": g_t("EMPURRADOR"), "BALSA": g_t("BALSA"),
                    "STATUS": p["STATUS"]["select"]["name"] if "STATUS" in p and p["STATUS"]["select"] else "---",
                    "DESCRIÇÃO": g_t("DESCRIÇÃO")
                })
            return lista
    except: return []
    return []

# --- NAVEGAÇÃO ---
if "pagina" not in st.session_state: st.session_state.pagina = "🏠 HOME"
if "dados_edicao" not in st.session_state: st.session_state.dados_edicao = None

def navegar(p): st.session_state.pagina = p; st.rerun()

# --- TELA HOME ---
if st.session_state.pagina == "🏠 HOME":
    if os.path.exists("LOGO.PNG"): st.image("LOGO.PNG", width=250)
    st.markdown("---")
    c1, c2, c3 = st.columns(3)
    with c1: 
        if st.button("📋 NOVO LANÇAMENTO"): st.session_state.dados_edicao = None; navegar("📋 CADASTRO")
    with c2: 
        if st.button("📊 VER AGENDAMENTOS"): navegar("📊 GRADE")
    with c3: 
        if st.button("💰 FINANCEIRO"): navegar("💰 FINANCEIRO")

# --- TELA CADASTRO (COM AJUSTE DE SALVAMENTO) ---
elif st.session_state.pagina == "📋 CADASTRO":
    edit = st.session_state.dados_edicao
    if st.button("⬅️ VOLTAR"): navegar("🏠 HOME")
    st.header("📝 Cadastro / Edição")
    with st.form("form_final"):
        c1, c2, c3 = st.columns(3)
        os_n = c1.text_input("Nº O.S", value=edit["Nº OS"] if edit else "")
        dt_s = c2.date_input("DT SAÍDA", format="DD/MM/YYYY")
        cli = c3.text_input("CLIENTE", value=edit["CLIENTE"] if edit else "")
        
        c4, c5, c6 = st.columns(3)
        ini = c4.date_input("INÍCIO DA MISSÃO", format="DD/MM/YYYY")
        fim = c5.date_input("FIM DA MISSÃO", format="DD/MM/YYYY")
        bal = c6.text_input("BALSA", value=edit["BALSA"] if edit else "")
        
        c7, c8, c9 = st.columns(3)
        h_emb = c7.text_input("HORA DE EMBARQUE")
        esc1 = c8.text_input("ESCOLTA 1")
        dest = c9.text_input("DESTINO")
        
        c10, c11, c12 = st.columns(3)
        loc = c10.text_input("LOCAL")
        esc2 = c11.text_input("ESCOLTA 2")
        ped = c12.text_input("PEDIDO")
        
        c13, c14, c15 = st.columns(3)
        emp = c13.text_input("EMPURRADOR", value=edit["EMPURRADOR"] if edit else "")
        ser = c14.selectbox("SERVIÇO", ["Escolta", "Vigilância"])
        ass = c15.text_input("ASSINATURA RESPONSÁVEL")
        
        obs = st.text_area("DESCRIÇÃO / OBSERVAÇÕES", value=edit["DESCRIÇÃO"] if edit else "")
        sts = st.selectbox("STATUS", ["Em Andamento", "Encerrado"])
        
        # AJUSTE: SALVAMENTO E RETORNO IMEDIATO
        if st.form_submit_button("✅ SALVAR OPERAÇÃO", type="primary"):
            payload = {
                "properties": {
                    "Nº OS": {"title": [{"text": {"content": os_n}}]},
                    "CLIENTE": {"rich_text": [{"text": {"content": cli}}]},
                    "DT SAÍDA": {"date": {"start": dt_s.strftime('%Y-%m-%d')}},
                    "EMPURRADOR": {"rich_text": [{"text": {"content": emp}}]},
                    "DESCRIÇÃO": {"rich_text": [{"text": {"content": obs}}]},
                    "STATUS": {"select": {"name": sts}}
                }
            }
            if edit:
                res = requests.patch(f"https://api.notion.com/v1/pages/{edit['ID']}", headers=headers, json=payload)
            else:
                payload["parent"] = {"database_id": DATABASE}
                res = requests.post("https://api.notion.com/v1/pages", headers=headers, json=payload)
            
            if res.status_code == 200:
                st.success("✅ OPERAÇÃO SALVA COM SUCESSO!")
                st.session_state.dados_edicao = None # Limpa cache de edição
                navegar("🏠 HOME") # Retorna para o início
            else:
                st.error(f"ERRO AO SALVAR: Verifique os nomes das colunas no Notion.")

# --- TELA GRADE ---
elif st.session_state.pagina == "📊 GRADE":
    if st.button("⬅️ VOLTAR"): navegar("🏠 HOME")
    st.subheader("📊 Agendamentos Ativos")
    dados = carregar_dados_notion()
    if dados:
        for d in dados:
            with st.expander(f"O.S: {d['Nº OS']} - {d['CLIENTE']}"):
                c1, c2 = st.columns([4, 1])
                c1.write(f"**Empurrador:** {d['EMPURRADOR']} | **Status:** {d['STATUS']}")
                if c2.button("✏️ Editar", key=f"ed_{d['ID']}"):
                    st.session_state.dados_edicao = d
                    navegar("📋 CADASTRO")
                pdf_b = gerar_pdf_transdourada(d)
                c2.download_button("📄 PDF", pdf_b, f"OS_{d['Nº OS']}.pdf", key=f"pdf_{d['ID']}")

elif st.session_state.pagina == "💰 FINANCEIRO":
    if st.button("⬅️ VOLTAR"): navegar("🏠 HOME")
    st.header("💰 Financeiro")
    st.table(pd.DataFrame(columns=["DATA", "PEDIDO", "VALOR", "STATUS"]))
