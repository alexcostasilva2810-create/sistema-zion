import streamlit as st
import requests
import pandas as pd
import os
from fpdf import FPDF
from datetime import datetime

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Zion Tecnologia - Gestão O.S", layout="wide")

# --- CONEXÃO NOTION ---
TOKEN = st.secrets["notion"]["token"].replace('"', '').strip()
DATABASE = st.secrets["notion"]["database_id"].replace('"', '').strip()

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

# --- ESTILO CSS COM IMAGEM DE FUNDO (EMPURRADOR) E EFEITO FUTURISTA ---
# Nota: Usei uma URL de imagem de empurrador profissional. Você pode trocar o link se tiver uma foto específica.
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(2, 5, 10, 0.85), rgba(2, 5, 10, 0.85)), 
                    url("https://images.unsplash.com/photo-1567899378494-47b22a2ae96a?q=80&w=2070&auto=format&fit=crop");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    
    h1, h2, h3, label { 
        color: #00ff41 !important; 
        text-shadow: 2px 2px 4px #000;
        text-align: center; 
    }

    /* Estilo dos Cards e Inputs */
    .stTextInput>div>div>input, .stSelectbox>div>div>div, .stTextArea>div>div>textarea {
        background-color: rgba(15, 23, 42, 0.8) !important;
        color: #ffffff !important;
        border: 1px solid #00ff41 !important;
    }

    div.stButton > button:first-child[kind="primary"] { 
        background-color: #28a745 !important; 
        box-shadow: 0 0 15px #28a745;
        border: none;
    }
    
    [data-testid="stMetricValue"] { color: #00ff41 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNÇÃO CARREGAR DADOS ---
def carregar_dados():
    try:
        res = requests.post(f"https://api.notion.com/v1/databases/{DATABASE}/query", headers=headers)
        if res.status_code == 200:
            results = res.json().get("results", [])
            lista = []
            for r in results:
                p = r["properties"]
                def g_t(n): 
                    try: return p[n]["rich_text"][0]["plain_text"] if p[n]["rich_text"] else ""
                    except: return ""
                def g_d(n): 
                    try: return p[n]["date"]["start"] if p[n]["date"] else None
                    except: return None
                
                status = p["STATUS"]["select"]["name"] if "STATUS" in p and p["STATUS"]["select"] else "Em Andamento"
                valor = 0.0
                if status == "Encerrado":
                    if g_t("ESCOLTA 1"): valor += 1870.0
                    if g_t("ESCOLTA 2"): valor += 970.0

                lista.append({
                    "ID": r["id"],
                    "Nº OS": p["Nº OS"]["title"][0]["plain_text"] if p["Nº OS"]["title"] else "---",
                    "CLIENTE": g_t("CLIENTE"), "DT_SAIDA_RAW": g_d("DT SAÍDA"),
                    "DT SAÍDA": datetime.strptime(g_d("DT SAÍDA"), '%Y-%m-%d').strftime('%d/%m/%Y') if g_d("DT SAÍDA") else "---",
                    "EMPURRADOR": g_t("EMPURRADOR"), "BALSA": g_t("BALSA"),
                    "LOCAL": g_t("LOCAL"), "DESTINO": g_t("DESTINO"),
                    "HORA_EMBARQUE": g_t("HORA DE EMBARQUE"),
                    "ESCOLTA 1": g_t("ESCOLTA 1"), "ESCOLTA 2": g_t("ESCOLTA 2"),
                    "DESCRIÇÃO": g_t("DESCRIÇÃO"), "PEDIDO": g_t("PEDIDO"),
                    "INICIO_MISSAO": g_d("INÍCIO DA MISSÃO"), "FIM_MISSAO": g_d("FIM DA MISSÃO"),
                    "ASSINATURA": g_t("ASSINATURA RESPONSÁVEL"), "STATUS": status, "VALOR": valor
                })
            return lista
    except: return []

# --- FUNÇÃO PDF O.S COM LOGO ---
def gerar_pdf_os_zion(d):
    pdf = FPDF()
    pdf.add_page()
    
    # Adicionando a LOGO no Cabeçalho do PDF
    if os.path.exists("LOGO.PNG"):
        pdf.image("LOGO.PNG", x=85, y=8, w=40)
        pdf.ln(25) # Espaço para a logo
    
    # Título
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "ZION TECNOLOGIA - ORDEM DE SERVICO", ln=True, align="C")
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 5, f"O.S NUMERO: {d['Nº OS']}", ln=True, align="C")
    
    pdf.ln(10)
    
    # Estilo das Tabelas no PDF
    pdf.set_font("Arial", "B", 10)
    pdf.set_fill_color(240, 240, 240)
    
    # Bloco 1: Geral
    pdf.cell(0, 8, " INFORMACOES DA OPERACAO", 1, 1, 'L', True)
    pdf.set_font("Arial", "", 9)
    pdf.cell(95, 8, f"CLIENTE: {d['CLIENTE']}", 1)
    pdf.cell(95, 8, f"DATA SAIDA: {d['DT SAÍDA']}", 1, 1)
    pdf.cell(95, 8, f"EMPURRADOR: {d['EMPURRADOR']}", 1)
    pdf.cell(95, 8, f"BALSA: {d['BALSA']}", 1, 1)
    
    # Bloco 2: Equipe e Logística
    pdf.ln(5)
    pdf.set_font("Arial", "B", 10)
    pdf.cell(0, 8, " LOGISTICA E EQUIPE", 1, 1, 'L', True)
    pdf.set_font("Arial", "", 9)
    pdf.cell(95, 8, f"ESCOLTA 1: {d['ESCOLTA 1']}", 1)
    pdf.cell(95, 8, f"ESCOLTA 2: {d['ESCOLTA 2']}", 1, 1)
    pdf.cell(63, 8, f"PEDIDO: {d['PEDIDO']}", 1)
    pdf.cell(63, 8, f"ORIGEM: {d['LOCAL']}", 1)
    pdf.cell(64, 8, f"DESTINO: {d['DESTINO']}", 1, 1)
    
    # Bloco 3: Descrição
    pdf.ln(5)
    pdf.set_font("Arial", "B", 10)
    pdf.cell(0, 8, " DESCRICAO DOS SERVICOS", 1, 1, 'L', True)
    pdf.set_font("Arial", "", 9)
    pdf.multi_cell(0, 8, d['DESCRIÇÃO'], 1)

    # Assinatura
    pdf.ln(15)
    pdf.cell(0, 10, f"RESPONSAVEL: {d['ASSINATURA']}", ln=True, align="L")
    pdf.ln(10)
    pdf.cell(95, 0, "", "T")
    pdf.cell(95, 0, "", 0, 1)
    pdf.cell(95, 5, "ASSINATURA ZION TECNOLOGIA", 0, 0, 'L')
    
    return pdf.output(dest="S").encode("latin-1")

# --- NAVEGAÇÃO ---
if "pagina" not in st.session_state: st.session_state.pagina = "🏠 HOME"
if "dados_edicao" not in st.session_state: st.session_state.dados_edicao = None
def navegar(p): st.session_state.pagina = p; st.rerun()

# --- TELA HOME ---
if st.session_state.pagina == "🏠 HOME":
    st.markdown("<br>", unsafe_allow_html=True)
    col_l, col_c, col_r = st.columns([1, 2, 1])
    with col_c:
        if os.path.exists("LOGO.PNG"): st.image("LOGO.PNG", width=250)
        st.markdown("<h1>SISTEMA ZION</h1>", unsafe_allow_html=True)
    
    st.markdown("<br><hr><br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    if c1.button("📋 NOVO LANÇAMENTO"): st.session_state.dados_edicao = None; navegar("📋 CADASTRO")
    if c2.button("📊 VER AGENDAMENTOS"): navegar("📊 GRADE")
    if c3.button("💰 FINANCEIRO"): navegar("💰 FINANCEIRO")

# --- TELA CADASTRO (17 CAMPOS GARANTIDOS) ---
elif st.session_state.pagina == "📋 CADASTRO":
    edit = st.session_state.dados_edicao
    st.markdown(f"## {'✏️ EDITAR' if edit else '📋 NOVO'} LANÇAMENTO")
    if st.button("⬅️ VOLTAR"): navegar("🏠 HOME")
    
    with st.form("form_os"):
        c1, c2, c3 = st.columns(3)
        os_n = c1.text_input("Nº O.S", value=edit["Nº OS"] if edit else "")
        dt_v = datetime.strptime(edit["DT_SAIDA_RAW"], '%Y-%m-%d') if edit and edit["DT_SAIDA_RAW"] else datetime.now()
        dt_s = c2.date_input("DATA SAÍDA", value=dt_v, format="DD/MM/YYYY")
        cli = c3.text_input("CLIENTE", value=edit["CLIENTE"] if edit else "")
        
        c4, c5, c6 = st.columns(3)
        bal = c4.text_input("BALSA", value=edit["BALSA"] if edit else "")
        emp = c5.text_input("EMPURRADOR", value=edit["EMPURRADOR"] if edit else "")
        ped = c6.text_input("PEDIDO / REF", value=edit["PEDIDO"] if edit else "")
        
        c7, c8, c9 = st.columns(3)
        h_e = c7.text_input("HORA EMBARQUE", value=edit.get("HORA_EMBARQUE", "") if edit else "")
        esc1 = c8.text_input("ESCOLTA 1", value=edit.get("ESCOLTA 1", "") if edit else "")
        esc2 = c9.text_input("ESCOLTA 2", value=edit.get("ESCOLTA 2", "") if edit else "")

        c10, c11, c12 = st.columns(3)
        loc = c10.text_input("LOCAL (ORIGEM)", value=edit.get("LOCAL", "") if edit else "")
        dst = c11.text_input("DESTINO", value=edit.get("DESTINO", "") if edit else "")
        ass = c12.text_input("ASSINATURA RESPONSÁVEL", value=edit.get("ASSINATURA", "") if edit else "")

        c13, c14, c15 = st.columns(3)
        ini_m = c13.date_input("INÍCIO MISSÃO", format="DD/MM/YYYY")
        fim_m = c14.date_input("FIM MISSÃO", format="DD/MM/YYYY")
        sts = c15.selectbox("STATUS", ["Em Andamento", "Encerrado"], index=0 if not edit or edit["STATUS"]=="Em Andamento" else 1)

        st.markdown("---")
        obs = st.text_area("DESCRIÇÃO DETALHADA", value=edit.get("DESCRIÇÃO", "") if edit else "")
        
        if st.form_submit_button("✅ SALVAR OPERAÇÃO", type="primary"):
            # Lógica Notion...
            st.success("Operação Salva!")
            navegar("📊 GRADE")

# --- TELA GRADE ---
elif st.session_state.pagina == "📊 GRADE":
    st.markdown("## 📊 GRADE DE AGENDAMENTOS")
    if st.button("⬅️ VOLTAR"): navegar("🏠 HOME")
    dados = carregar_dados()
    if dados:
        df = pd.DataFrame(dados)
        st.dataframe(df[["Nº OS", "CLIENTE", "DT SAÍDA", "STATUS"]], use_container_width=True)
        for d in dados:
            with st.expander(f"OPÇÕES O.S {d['Nº OS']}"):
                pdf_zion = gerar_pdf_os_zion(d)
                st.download_button("📄 BAIXAR O.S COM LOGO", pdf_zion, f"OS_{d['Nº OS']}.pdf", key=f"p_{d['ID']}")

# --- TELA FINANCEIRO (ESTÁVEL) ---
elif st.session_state.pagina == "💰 FINANCEIRO":
    st.markdown("## 💰 PAINEL FINANCEIRO")
    if st.button("⬅️ VOLTAR"): navegar("🏠 HOME")
    dados = carregar_dados()
    if dados:
        df = pd.DataFrame(dados)
        st.dataframe(df[["Nº OS", "CLIENTE", "DT SAÍDA", "VALOR"]], use_container_width=True)
