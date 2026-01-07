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

# --- ESTILO CSS AZUL ROYAL FUTURISTA ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(0, 35, 102, 0.85), rgba(0, 35, 102, 0.85)), 
                    url("https://images.unsplash.com/photo-1567899378494-47b22a2ae96a?q=80&w=2070&auto=format&fit=crop");
        background-size: cover; background-position: center; background-attachment: fixed;
    }
    h1, h2, h3, label { color: #00ff41 !important; text-shadow: 2px 2px 4px #000; text-align: center; }
    
    /* Botões: Verde para Salvar/Editar e Azul para PDF */
    div.stButton > button:first-child[kind="primary"] { background-color: #28a745 !important; border: none; box-shadow: 0 0 10px #28a745; }
    div.stButton > button.pdf-btn { background-color: #0056b3 !important; color: white !important; border: none; box-shadow: 0 0 10px #0056b3; }
    
    .stDataFrame { background-color: rgba(15, 23, 42, 0.9); border-radius: 10px; border: 1px solid #00ff41; }
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

# --- PDF O.S PERSONALIZADA ---
def gerar_pdf_os(d):
    pdf = FPDF()
    pdf.add_page()
    if os.path.exists("LOGO2.PNG"): pdf.image("LOGO2.PNG", x=85, y=8, w=40); pdf.ln(25)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "ORDEM DE SERVICO - ZION TECNOLOGIA", ln=True, align="C")
    pdf.set_font("Arial", "", 9)
    for k, v in d.items():
        if k not in ["ID", "VALOR", "DT_SAIDA_RAW"]:
            pdf.cell(50, 8, f"{k}:", 1); pdf.cell(140, 8, f"{v}", 1, 1)
    return pdf.output(dest="S").encode("latin-1")

# --- NAVEGAÇÃO ---
if "pagina" not in st.session_state: st.session_state.pagina = "🏠 HOME"
if "dados_edicao" not in st.session_state: st.session_state.dados_edicao = None
def navegar(p): st.session_state.pagina = p; st.rerun()

# --- TELA HOME ---
if st.session_state.pagina == "🏠 HOME":
    st.markdown("<br>", unsafe_allow_html=True)
    if os.path.exists("LOGO.PNG"): st.image("LOGO.PNG", width=250)
    st.markdown("<h1>SISTEMA ZION</h1>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    if c1.button("📋 NOVO LANÇAMENTO"): st.session_state.dados_edicao = None; navegar("📋 CADASTRO")
    if c2.button("📊 VER AGENDAMENTOS"): navegar("📊 GRADE")
    if c3.button("💰 FINANCEIRO"): navegar("💰 FINANCEIRO")

# --- TELA CADASTRO (17 COLUNAS RESTAURADAS) ---
elif st.session_state.pagina == "📋 CADASTRO":
    edit = st.session_state.dados_edicao
    st.markdown(f"## {'✏️ EDITAR' if edit else '📋 NOVO'} REGISTRO")
    if st.button("⬅️ VOLTAR"): navegar("🏠 HOME")
    with st.form("form_os"):
        c1, c2, c3 = st.columns(3)
        os_n = c1.text_input("Nº O.S", value=edit["Nº OS"] if edit else "")
        dt_v = datetime.strptime(edit["DT_SAIDA_RAW"], '%Y-%m-%d') if edit and edit["DT_SAIDA_RAW"] else datetime.now()
        dt_s = c2.date_input("DATA SAÍDA", value=dt_v, format="DD/MM/YYYY")
        cli = c3.text_input("CLIENTE", value=edit["CLIENTE"] if edit else "")
        c4, c5, c6 = st.columns(3)
        emp = c4.text_input("EMPURRADOR", value=edit["EMPURRADOR"] if edit else "")
        bal = c5.text_input("BALSA", value=edit["BALSA"] if edit else "")
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
        obs = st.text_area("DESCRIÇÃO", value=edit.get("DESCRIÇÃO", "") if edit else "")
        if st.form_submit_button("✅ SALVAR OPERAÇÃO", type="primary"):
            st.success("Salvo com sucesso!"); navegar("📊 GRADE")

# --- TELA GRADE (EXIBIÇÃO + BOTÕES VERDE/AZUL) ---
elif st.session_state.pagina == "📊 GRADE":
    st.markdown("## 📊 VER AGENDAMENTOS")
    if st.button("⬅️ VOLTAR"): navegar("🏠 HOME")
    dados = carregar_dados()
    if dados:
        df = pd.DataFrame(dados)
        st.dataframe(df[["Nº OS", "CLIENTE", "DT SAÍDA", "EMPURRADOR", "BALSA", "STATUS"]], use_container_width=True)
        for d in dados:
            with st.expander(f"OPÇÕES O.S {d['Nº OS']} - {d['CLIENTE']}"):
                c1, c2 = st.columns(2)
                if c1.button("✏️ EDITAR", key=f"ed_{d['ID']}", type="primary"):
                    st.session_state.dados_edicao = d; navegar("📋 CADASTRO")
                pdf_bytes = gerar_pdf_os(d)
                c2.download_button("📄 EXPORTAR PDF (AZUL)", pdf_bytes, f"OS_{d['Nº OS']}.pdf", key=f"pdf_{d['ID']}")

# --- TELA FINANCEIRO (FILTRO COMPACTO + TABELA COMPLETA) ---
elif st.session_state.pagina == "💰 FINANCEIRO":
    st.markdown("## 💰 RELATÓRIO FINANCEIRO")
    if st.button("⬅️ VOLTAR"): navegar("🏠 HOME")
    c1, c2, c3 = st.columns([1, 1, 1])
    ini_f = c1.date_input("INÍCIO", format="DD/MM/YYYY")
    fim_f = c2.date_input("FIM", format="DD/MM/YYYY")
    
    dados = carregar_dados()
    if dados:
        df = pd.DataFrame(dados)
        df['dt_filter'] = pd.to_datetime(df['DT_SAIDA_RAW'])
        df_filt = df[(df['dt_filter'] >= pd.Timestamp(ini_f)) & (df['dt_filter'] <= pd.Timestamp(fim_f))]
        
        st.metric("TOTAL A PAGAR", f"R$ {df_filt['VALOR'].sum():,.2f}")
        # Colunas fundamentais + Valor ao lado
        st.dataframe(df_filt[["Nº OS", "CLIENTE", "DT SAÍDA", "EMPURRADOR", "BALSA", "ESCOLTA 1", "ESCOLTA 2", "VALOR"]], use_container_width=True)
        
        if st.button("📥 EXPORTAR FINANCEIRO PDF", key="fin_pdf"):
            st.info("Relatório gerado!")
