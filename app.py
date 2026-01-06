import streamlit as st
import requests
import pandas as pd
import os
from fpdf import FPDF
from datetime import datetime

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

# --- ESTILO CSS (BOTÃO VERDE E DESIGN) ---
st.markdown("""
    <style>
    div.stButton > button:first-child[kind="primary"] { background-color: #28a745 !important; color: white !important; }
    .stButton>button { width: 100%; border-radius: 8px; font-weight: bold; height: 3.5em; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNÇÃO GERAR PDF (MODELO TRANSDOURADA) ---
def gerar_pdf_transdourada(d):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 10)
    pdf.cell(0, 5, "ZION TECNOLOGIA | TRANSDOURADA", ln=True)
    pdf.ln(10)
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Solicitação de Escolta", ln=True, align="C")
    pdf.cell(0, 7, f"O.S: {d.get('Nº OS', '---')}", ln=True, align="C")
    pdf.ln(5)
    pdf.set_font("Arial", "B", 11)
    pdf.cell(0, 10, f"SOLICITANTE ( {d.get('CLIENTE', '---').upper()} )", border=1, ln=True, align="C")
    pdf.ln(5)
    pdf.set_font("Arial", "", 10)
    pdf.multi_cell(0, 6, f"EMPURRADOR: {d.get('EMPURRADOR', '---')}\nBALSA: {d.get('BALSA', '---')}\nLOCAL: {d.get('LOCAL', '---')}\nDESTINO: {d.get('DESTINO', '---')}\nDESCRIÇÃO: {d.get('DESCRIÇÃO', '---')}")
    pdf.set_y(-35)
    pdf.set_font("Arial", "B", 7)
    pdf.cell(0, 5, "TRANSDOURADA NAVEGAÇÃO LTDA - ANANINDEUA/PA", ln=True, align="C")
    return pdf.output(dest="S").encode("latin-1")

# --- FUNÇÃO PUXAR DADOS DO NOTION (CORRIGIDA) ---
def carregar_dados_notion():
    try:
        url = f"https://api.notion.com/v1/databases/{DATABASE}/query"
        res = requests.post(url, headers=headers)
        if res.status_code == 200:
            results = res.json().get("results", [])
            lista = []
            for r in results:
                p = r["properties"]
                # Extração segura de texto e data
                def get_t(prop): return p[prop]["rich_text"][0]["plain_text"] if prop in p and p[prop]["rich_text"] else "---"
                def get_title(prop): return p[prop]["title"][0]["plain_text"] if prop in p and p[prop]["title"] else "---"
                def get_d(prop): 
                    dt = p[prop]["date"]["start"] if prop in p and p[prop]["date"] else None
                    return datetime.strptime(dt, '%Y-%m-%d').strftime('%d/%m/%Y') if dt else "---"
                
                lista.append({
                    "ID_NOTION": r["id"],
                    "Nº OS": get_title("Nº OS"),
                    "CLIENTE": get_t("CLIENTE"),
                    "DT SAÍDA": get_d("DT SAÍDA"),
                    "INÍCIO": get_d("INÍCIO DA MISSÃO"),
                    "EMPURRADOR": get_t("EMPURRADOR"),
                    "BALSA": get_t("BALSA"),
                    "LOCAL": get_t("LOCAL"),
                    "DESTINO": get_t("DESTINO"),
                    "DESCRIÇÃO": get_t("DESCRIÇÃO"),
                    "STATUS": p["STATUS"]["select"]["name"] if "STATUS" in p and p["STATUS"]["select"] else "---"
                })
            return lista
        return []
    except: return []

# --- NAVEGAÇÃO ---
if "pagina" not in st.session_state: st.session_state.pagina = "🏠 HOME"
if "dados_edicao" not in st.session_state: st.session_state.dados_edicao = None

def navegar(p):
    st.session_state.pagina = p
    st.rerun()

# --- TELA HOME ---
if st.session_state.pagina == "🏠 HOME":
    if os.path.exists("LOGO.PNG"): st.image("LOGO.PNG", width=250)
    st.title("🛡️ Sistema Zion - Transdourada")
    st.markdown("---")
    c1, c2, c3 = st.columns(3)
    with c1: 
        if st.button("📋 NOVO LANÇAMENTO"): st.session_state.dados_edicao = None; navegar("📋 CADASTRO")
    with c2: 
        if st.button("📊 VER AGENDAMENTOS"): navegar("📊 GRADE")
    with c3: 
        if st.button("💰 FINANCEIRO"): navegar("💰 FINANCEIRO")

# --- TELA DE CADASTRO (17 CAMPOS CONGELADOS) ---
elif st.session_state.pagina == "📋 CADASTRO":
    edit = st.session_state.dados_edicao
    if st.button("⬅️ VOLTAR"): navegar("🏠 HOME")
    st.header("📝 Cadastro / Edição de Missão")
    with st.form("form_missao"):
        c1, c2, c3 = st.columns(3)
        os_n = c1.text_input("Nº O.S", value=edit["Nº OS"] if edit else "")
        dt_saida = c2.date_input("DT SAÍDA", format="DD/MM/YYYY")
        cliente = c3.text_input("CLIENTE", value=edit["CLIENTE"] if edit else "")
        
        c4, c5, c6 = st.columns(3)
        ini_m = c4.date_input("INÍCIO DA MISSÃO", format="DD/MM/YYYY")
        fim_m = c5.date_input("FIM DA MISSÃO", format="DD/MM/YYYY")
        balsa = c6.text_input("BALSA", value=edit["BALSA"] if edit else "")
        
        c7, c8, c9 = st.columns(3)
        h_emb = c7.text_input("HORA DE EMBARQUE")
        esc1 = c8.text_input("ESCOLTA 1")
        destino = c9.text_input("DESTINO", value=edit["DESTINO"] if edit else "")
        
        c10, c11, c12 = st.columns(3)
        local = c10.text_input("LOCAL", value=edit["LOCAL"] if edit else "")
        esc2 = c11.text_input("ESCOLTA 2")
        pedido = c12.text_input("PEDIDO")
        
        c13, c14, c15 = st.columns(3)
        empurrador = c13.text_input("EMPURRADOR", value=edit["EMPURRADOR"] if edit else "")
        servico = c14.selectbox("SERVIÇO", ["Escolta", "Vigilância"])
        ass_resp = c15.text_input("ASSINATURA RESPONSÁVEL")
        
        desc = st.text_area("DESCRIÇÃO / OBSERVAÇÕES", value=edit["DESCRIÇÃO"] if edit else "")
        status = st.selectbox("STATUS", ["Em Andamento", "Encerrado"])
        
        if st.form_submit_button("✅ SALVAR OPERAÇÃO", type="primary"):
            payload = {
                "properties": {
                    "Nº OS": {"title": [{"text": {"content": os_n}}]},
                    "CLIENTE": {"rich_text": [{"text": {"content": cliente}}]},
                    "DT SAÍDA": {"date": {"start": dt_saida.strftime('%Y-%m-%d')}},
                    "INÍCIO DA MISSÃO": {"date": {"start": ini_m.strftime('%Y-%m-%d')}},
                    "EMPURRADOR": {"rich_text": [{"text": {"content": empurrador}}]},
                    "BALSA": {"rich_text": [{"text": {"content": balsa}}]},
                    "LOCAL": {"rich_text": [{"text": {"content": local}}]},
                    "DESTINO": {"rich_text": [{"text": {"content": destino}}]},
                    "DESCRIÇÃO": {"rich_text": [{"text": {"content": desc}}]},
                    "STATUS": {"select": {"name": status}}
                }
            }
            if edit:
                res = requests.patch(f"https://api.notion.com/v1/pages/{edit['ID_NOTION']}", headers=headers, json=payload)
            else:
                payload["parent"] = {"database_id": DATABASE}
                res = requests.post("https://api.notion.com/v1/pages", headers=headers, json=payload)
            
            if res.status_code == 200: st.success("Salvo!"); navegar("🏠 HOME")
            else: st.error(f"Erro: {res.text}")

# --- TELA GRADE (RESTAURADA) ---
elif st.session_state.pagina == "📊 GRADE":
    if st.button("⬅️ VOLTAR"): navegar("🏠 HOME")
    st.subheader("📊 Agendamentos Ativos")
    dados = carregar_dados_notion()
    if dados:
        for d in dados:
            with st.expander(f"O.S: {d['Nº OS']} - {d['CLIENTE']} | Saída: {d['DT SAÍDA']}"):
                c1, c2 = st.columns([4, 1])
                c1.write(f"**Empurrador:** {d['EMPURRADOR']} | **Balsa:** {d['BALSA']} | **Status:** {d['STATUS']}")
                if c2.button("✏️ Editar", key=f"ed_{d['ID_NOTION']}"):
                    st.session_state.dados_edicao = d
                    navegar("📋 CADASTRO")
                pdf_b = gerar_pdf_transdourada(d)
                c2.download_button("📄 PDF", pdf_b, f"OS_{d['Nº OS']}.pdf", key=f"pdf_{d['ID_NOTION']}")
    else: st.info("Buscando dados no Notion... Se não aparecer nada, verifique a conexão.")

# --- TELA FINANCEIRO ---
elif st.session_state.pagina == "💰 FINANCEIRO":
    if st.button("⬅️ VOLTAR"): navegar("🏠 HOME")
    st.header("💰 Financeiro")
    st.table(pd.DataFrame(columns=["DATA", "PEDIDO", "VALOR", "STATUS"]))
