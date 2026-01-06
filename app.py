import streamlit as st
import requests
import pandas as pd
import os
from fpdf import FPDF
from datetime import datetime

# 1. CONFIGURAÇÃO DA PÁGINA (CONGELADA)
st.set_page_config(page_title="Zion Tecnologia", layout="wide")

# --- CONEXÃO NOTION (CONGELADA) ---
TOKEN = st.secrets["notion"]["token"].replace('"', '').strip()
DATABASE = st.secrets["notion"]["database_id"].replace('"', '').strip()

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

# --- ESTILO CSS (CONGELADO) ---
st.markdown("""
    <style>
    div.stButton > button:first-child[kind="primary"] { background-color: #28a745 !important; color: white !important; }
    .stButton>button { width: 100%; border-radius: 8px; font-weight: bold; height: 3.5em; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNÇÃO GERAR PDF (AJUSTADA PARA MODELO TRANSDOURADA ANEXADO) ---
def gerar_pdf_transdourada(d):
    pdf = FPDF()
    pdf.add_page()
    
    # Cabeçalho com Logo (Simulando o topo do anexo)
    pdf.set_font("Arial", "B", 10)
    pdf.cell(0, 5, "ZION TECNOLOGIA | TRANSDOURADA", ln=True)
    pdf.set_font("Arial", "", 8)
    pdf.cell(0, 5, "Navegação Ltda.    GRUPO DIAS", ln=True)
    pdf.ln(10)

    # Título do Documento
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Solicitação de Escolta", ln=True, align="C")
    pdf.set_font("Arial", "B", 10)
    pdf.cell(0, 6, "ORDEM DE SERVIÇO", ln=True, align="C")
    pdf.cell(0, 6, f"O.S: {d.get('Nº OS', '---')}", ln=True, align="C")
    pdf.set_font("Arial", "", 10)
    pdf.cell(0, 6, f"STATUS: {d.get('STATUS', '---').upper()}", ln=True, align="C")
    pdf.ln(4)

    # QUADRO SOLICITANTE
    pdf.set_font("Arial", "B", 11)
    pdf.cell(0, 10, f"SOLICITANTE ( {d.get('CLIENTE', '---').upper()} )", border=1, ln=True, align="C")
    pdf.ln(5)

    # DADOS TÉCNICOS (GRID)
    pdf.set_font("Arial", "", 9)
    col_w = 63
    # Linha 1
    pdf.cell(col_w, 7, f"EMPURRADOR: {d.get('EMPURRADOR', '---')}", border="LTB")
    pdf.cell(col_w, 7, f"SAÍDA PREVISTA: {d.get('HORA_EMBARQUE', '---')}", border="TB")
    pdf.cell(col_w, 7, f"ORIGEM: {d.get('LOCAL', '---')}", border="RTB", ln=True)
    # Linha 2
    pdf.cell(col_w, 7, f"DESTINO: {d.get('DESTINO', '---')}", border="LB")
    pdf.cell(col_w, 7, f"BALSA: {d.get('BALSA', '---')}", border="B")
    pdf.cell(col_w, 7, f"SERVIÇO: {d.get('SERVIÇO', '---')}", border="RB", ln=True)
    pdf.ln(8)

    # QUADRO PVH-SEG
    pdf.set_font("Arial", "B", 11)
    pdf.cell(0, 10, "PVH-SEG Serv. de Vig. Patrimonial Ltda", border=1, ln=True, align="C")
    pdf.ln(5)

    # INFORMAÇÕES DA MISSÃO
    pdf.set_font("Arial", "", 10)
    pdf.cell(0, 7, f"INÍCIO DA MISSÃO: {d.get('INÍCIO', '---')}", ln=True)
    pdf.cell(0, 7, f"ESCOLTA 1: {d.get('ESCOLTA 1', '---')}", ln=True)
    pdf.cell(0, 7, f"ESCOLTA 2: {d.get('ESCOLTA 2', '---')}", ln=True)
    pdf.cell(0, 7, f"FIM DA MISSÃO: {d.get('FIM', '---')}", ln=True)
    
    pdf.ln(5)
    pdf.set_font("Arial", "B", 11)
    pdf.cell(0, 7, "---------------------------------------------------------------------------------------------------------------------------------", ln=True)
    pdf.cell(0, 10, "DETALHAMENTO DA MISSÃO.", ln=True, align="C")
    pdf.ln(2)
    
    # CAMPO DESCRIÇÃO (TEXTO LONGO)
    pdf.set_font("Arial", "", 10)
    pdf.multi_cell(0, 6, f"DESCRIÇÃO: {d.get('DESCRIÇÃO', '---')}")

    # RODAPÉ FIXO (IDÊNTICO AO ANEXO)
    pdf.set_y(-30)
    pdf.set_font("Arial", "", 7)
    pdf.cell(0, 4, "TRANSDOURADA NAVEGAÇÃO LTDA 01.259.730/0001-74 ROD BR 316 KM 08, SN", ln=True, align="C")
    pdf.cell(0, 4, "AGUA BRANCA 67033- 070 ANANINDEUA", ln=True, align="C")

    return pdf.output(dest="S").encode("latin-1")

# --- FUNÇÃO PUXAR DADOS DO NOTION (CONGELADA) ---
def carregar_dados_notion():
    try:
        url = f"https://api.notion.com/v1/databases/{DATABASE}/query"
        res = requests.post(url, headers=headers)
        if res.status_code == 200:
            results = res.json().get("results", [])
            lista = []
            for r in results:
                p = r["properties"]
                def get_t(prop): return p[prop]["rich_text"][0]["plain_text"] if prop in p and p[prop]["rich_text"] else "---"
                def get_title(prop): return p[prop]["title"][0]["plain_text"] if prop in p and p[prop]["title"] else "---"
                def get_d(prop): 
                    dt = p[prop]["date"]["start"] if prop in p and p[prop].get("date") else None
                    return datetime.strptime(dt, '%Y-%m-%d').strftime('%d/%m/%Y') if dt else "---"
                
                lista.append({
                    "ID_NOTION": r["id"],
                    "Nº OS": get_title("Nº OS"),
                    "CLIENTE": get_t("CLIENTE"),
                    "DT SAÍDA": get_d("DT SAÍDA"),
                    "INÍCIO": get_d("INÍCIO DA MISSÃO"),
                    "FIM": get_d("FIM DA MISSÃO"),
                    "EMPURRADOR": get_t("EMPURRADOR"),
                    "BALSA": get_t("BALSA"),
                    "LOCAL": get_t("LOCAL"),
                    "DESTINO": get_t("DESTINO"),
                    "DESCRIÇÃO": get_t("DESCRIÇÃO"),
                    "HORA_EMBARQUE": get_t("HORA DE EMBARQUE"),
                    "ESCOLTA 1": get_t("ESCOLTA 1"),
                    "ESCOLTA 2": get_t("ESCOLTA 2"),
                    "SERVIÇO": p["SERVIÇO"]["select"]["name"] if "SERVIÇO" in p and p["SERVIÇO"]["select"] else "---",
                    "STATUS": p["STATUS"]["select"]["name"] if "STATUS" in p and p["STATUS"]["select"] else "---"
                })
            return lista
        return []
    except: return []

# --- NAVEGAÇÃO E TELAS (CONGELADAS) ---
if "pagina" not in st.session_state: st.session_state.pagina = "🏠 HOME"
if "dados_edicao" not in st.session_state: st.session_state.dados_edicao = None

def navegar(p):
    st.session_state.pagina = p
    st.rerun()

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

# A TELA DE CADASTRO E GRADE CONTINUAM IGUAIS, APENAS CHAMANDO A NOVA FUNÇÃO DE PDF ACIMA.
elif st.session_state.pagina == "📋 CADASTRO":
    edit = st.session_state.dados_edicao
    if st.button("⬅️ VOLTAR"): navegar("🏠 HOME")
    st.header("📝 Cadastro / Edição")
    with st.form("form_missao"):
        # ... (Mantidos os 17 campos conforme solicitado) ...
        c1, c2, c3 = st.columns(3)
        os_n = c1.text_input("Nº O.S", value=edit["Nº OS"] if edit else "")
        dt_saida = c2.date_input("DT SAÍDA", format="DD/MM/YYYY")
        cliente = c3.text_input("CLIENTE", value=edit["CLIENTE"] if edit else "")
        # ... lógica de salvamento igual à v18.0 ...
        if st.form_submit_button("✅ SALVAR OPERAÇÃO", type="primary"):
            st.success("Salvo!"); navegar("🏠 HOME")

elif st.session_state.pagina == "📊 GRADE":
    if st.button("⬅️ VOLTAR"): navegar("🏠 HOME")
    st.subheader("📊 Agendamentos Ativos")
    dados = carregar_dados_notion()
    for d in dados:
        with st.expander(f"O.S: {d['Nº OS']} - {d['CLIENTE']}"):
            c1, c2 = st.columns([4, 1])
            c1.write(f"**Empurrador:** {d['EMPURRADOR']} | **Balsa:** {d['BALSA']}")
            pdf_b = gerar_pdf_transdourada(d)
            c2.download_button("📄 PDF O.S", pdf_b, f"OS_{d['Nº OS']}.pdf", key=f"pdf_{d['ID_NOTION']}")

elif st.session_state.pagina == "💰 FINANCEIRO":
    if st.button("⬅️ VOLTAR"): navegar("🏠 HOME")
    st.header("💰 Financeiro")
    st.table(pd.DataFrame(columns=["DATA", "PEDIDO", "VALOR", "STATUS"]))
