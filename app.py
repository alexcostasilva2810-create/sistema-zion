import streamlit as st
import requests
import pandas as pd
import os
from fpdf import FPDF
from datetime import datetime

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Zion Tecnologia - Transdourada", layout="wide")

# --- CONEXÃO NOTION (Ajuste os secrets no Streamlit) ---
TOKEN = st.secrets["notion"]["token"].replace('"', '').strip()
DATABASE = st.secrets["notion"]["database_id"].replace('"', '').strip()

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

# --- ESTILO CSS (BOTÃO VERDE E INTERFACE) ---
st.markdown("""
    <style>
    div.stButton > button:first-child[kind="primary"] { background-color: #28a745 !important; color: white !important; border: none; }
    .stButton>button { width: 100%; border-radius: 8px; font-weight: bold; height: 3.5em; }
    [data-testid="stMetricValue"] { font-size: 1.8rem; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNÇÃO GERAR PDF (LAYOUT OFICIAL TRANSDOURADA) ---
def gerar_pdf_transdourada(d):
    pdf = FPDF()
    pdf.add_page()
    
    # Cabeçalho e Logo
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 5, "TRANSDOURADA NAVEGAÇÃO LTDA", ln=True, align="L")
    pdf.set_font("Arial", "", 8)
    pdf.cell(0, 5, "GRUPO DIAS - PVH SEG", ln=True, align="L")
    pdf.ln(10)

    # Título da O.S
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Solicitação de Escolta / Ordem de Serviço", ln=True, align="C")
    pdf.set_font("Arial", "B", 10)
    pdf.cell(0, 7, f"O.S Nº: {d.get('Nº OS', '---')} | STATUS: {d.get('STATUS', '---').upper()}", ln=True, align="C")
    pdf.ln(5)

    # QUADRO 1: SOLICITANTE
    pdf.set_fill_color(240, 240, 240)
    pdf.set_font("Arial", "B", 11)
    pdf.cell(0, 10, f"DADOS DO SOLICITANTE: {d.get('CLIENTE', '---').upper()}", border=1, ln=True, align="L", fill=True)
    
    # QUADRO 2: GRID TÉCNICO
    pdf.set_font("Arial", "", 9)
    # Linha A
    pdf.cell(95, 8, f"EMPURRADOR: {d.get('EMPURRADOR', '---')}", border=1)
    pdf.cell(95, 8, f"BALSA: {d.get('BALSA', '---')}", border=1, ln=True)
    # Linha B
    pdf.cell(95, 8, f"ORIGEM (LOCAL): {d.get('LOCAL', '---')}", border=1)
    pdf.cell(95, 8, f"DESTINO: {d.get('DESTINO', '---')}", border=1, ln=True)
    # Linha C
    pdf.cell(95, 8, f"HORA DE EMBARQUE: {d.get('HORA_EMBARQUE', '---')}", border=1)
    pdf.cell(95, 8, f"PEDIDO: {d.get('PEDIDO', '---')}", border=1, ln=True)
    pdf.ln(5)

    # QUADRO 3: PVH-SEG (EQUIPE E MISSÃO)
    pdf.set_font("Arial", "B", 11)
    pdf.cell(0, 10, "DETALHAMENTO DA MISSÃO - EQUIPE PVH-SEG", border=1, ln=True, align="C", fill=True)
    pdf.set_font("Arial", "", 10)
    pdf.cell(95, 8, f"INÍCIO: {d.get('INÍCIO', '---')}", border=1)
    pdf.cell(95, 8, f"FIM: {d.get('FIM', '---')}", border=1, ln=True)
    pdf.cell(95, 8, f"ESCOLTA 1: {d.get('ESCOLTA 1', '---')}", border=1)
    pdf.cell(95, 8, f"ESCOLTA 2: {d.get('ESCOLTA 2', '---')}", border=1, ln=True)
    
    pdf.ln(5)
    pdf.set_font("Arial", "B", 10)
    pdf.cell(0, 7, "DESCRIÇÃO DOS SERVIÇOS:", ln=True)
    pdf.set_font("Arial", "", 10)
    pdf.multi_cell(0, 6, d.get('DESCRIÇÃO', '---'), border=1)
    
    # Assinatura
    pdf.ln(15)
    pdf.cell(95, 0.1, "", border="T") # Linha para assinar
    pdf.set_x(110)
    pdf.cell(85, 0.1, "", border="T", ln=True)
    pdf.cell(95, 7, f"Resp: {d.get('ASSINATURA', '---')}", ln=False, align="C")
    pdf.set_x(110)
    pdf.cell(85, 7, "Fiscalização Zion", ln=True, align="C")

    # Rodapé
    pdf.set_y(-25)
    pdf.set_font("Arial", "I", 7)
    pdf.cell(0, 4, "Documento gerado pelo Sistema Zion Tecnologia - Transdourada Navegação Ltda", ln=True, align="C")
    
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
                def g_d(n): 
                    try: return datetime.strptime(p[n]["date"]["start"], '%Y-%m-%d').strftime('%d/%m/%Y') if n in p and p[n]["date"] else "---"
                    except: return "---"
                
                lista.append({
                    "ID": r["id"],
                    "Nº OS": p["Nº OS"]["title"][0]["plain_text"] if p["Nº OS"]["title"] else "---",
                    "CLIENTE": g_t("CLIENTE"), "DT SAÍDA": g_d("DT SAÍDA"),
                    "INÍCIO": g_d("INÍCIO DA MISSÃO"), "FIM": g_d("FIM DA MISSÃO"),
                    "EMPURRADOR": g_t("EMPURRADOR"), "BALSA": g_t("BALSA"),
                    "LOCAL": g_t("LOCAL"), "DESTINO": g_t("DESTINO"),
                    "HORA_EMBARQUE": g_t("HORA DE EMBARQUE"),
                    "ESCOLTA 1": g_t("ESCOLTA 1"), "ESCOLTA 2": g_t("ESCOLTA 2"),
                    "DESCRIÇÃO": g_t("DESCRIÇÃO"), "PEDIDO": g_t("PEDIDO"),
                    "ASSINATURA": g_t("ASSINATURA RESPONSÁVEL"),
                    "STATUS": p["STATUS"]["select"]["name"] if "STATUS" in p and p["STATUS"]["select"] else "---"
                })
            return lista
    except: return []

# --- NAVEGAÇÃO ---
if "pagina" not in st.session_state: st.session_state.pagina = "🏠 HOME"
if "dados_edicao" not in st.session_state: st.session_state.dados_edicao = None

def navegar(p): st.session_state.pagina = p; st.rerun()

# --- TELA HOME ---
if st.session_state.pagina == "🏠 HOME":
    if os.path.exists("LOGO.PNG"): st.image("LOGO.PNG", width=250)
    st.title("🛡️ Sistema Zion - Gestão Operacional")
    st.markdown("---")
    c1, c2, c3 = st.columns(3)
    with c1: 
        if st.button("📋 NOVO LANÇAMENTO"): st.session_state.dados_edicao = None; navegar("📋 CADASTRO")
    with c2: 
        if st.button("📊 VER AGENDAMENTOS"): navegar("📊 GRADE")
    with c3: 
        if st.button("💰 FINANCEIRO"): navegar("💰 FINANCEIRO")

# --- TELA CADASTRO (17 CAMPOS INTEGRADOS) ---
elif st.session_state.pagina == "📋 CADASTRO":
    edit = st.session_state.dados_edicao
    if st.button("⬅️ CANCELAR E VOLTAR"): navegar("🏠 HOME")
    st.header("📝 Formulário de Ordem de Serviço")
    
    with st.form("form_os"):
        c1, c2, c3 = st.columns(3)
        os_n = c1.text_input("Nº O.S", value=edit["Nº OS"] if edit else "")
        dt_s = c2.date_input("DATA DE SAÍDA", format="DD/MM/YYYY")
        cli = c3.text_input("CLIENTE", value=edit["CLIENTE"] if edit else "")
        
        c4, c5, c6 = st.columns(3)
        ini = c4.date_input("INÍCIO DA MISSÃO", format="DD/MM/YYYY")
        fim = c5.date_input("FIM DA MISSÃO", format="DD/MM/YYYY")
        bal = c6.text_input("BALSA", value=edit["BALSA"] if edit else "")
        
        c7, c8, c9 = st.columns(3)
        h_emb = c7.text_input("HORA DE EMBARQUE", value=edit.get("HORA_EMBARQUE", "") if edit else "")
        esc1 = c8.text_input("ESCOLTA 1", value=edit.get("ESCOLTA 1", "") if edit else "")
        dest = c9.text_input("DESTINO", value=edit.get("DESTINO", "") if edit else "")
        
        c10, c11, c12 = st.columns(3)
        loc = c10.text_input("LOCAL (ORIGEM)", value=edit.get("LOCAL", "") if edit else "")
        esc2 = c11.text_input("ESCOLTA 2", value=edit.get("ESCOLTA 2", "") if edit else "")
        ped = c12.text_input("PEDIDO / REF", value=edit.get("PEDIDO", "") if edit else "")
        
        c13, c14, c15 = st.columns(3)
        emp = c13.text_input("EMPURRADOR", value=edit.get("EMPURRADOR", "") if edit else "")
        ass = c14.text_input("ASSINATURA RESPONSÁVEL", value=edit.get("ASSINATURA", "") if edit else "")
        sts = c15.selectbox("STATUS", ["Em Andamento", "Encerrado"])
        
        obs = st.text_area("DESCRIÇÃO DETALHADA", value=edit.get("DESCRIÇÃO", "") if edit else "")
        
        if st.form_submit_button("✅ SALVAR OPERAÇÃO", type="primary"):
            payload = {"properties": {
                "Nº OS": {"title": [{"text": {"content": str(os_n)}}]},
                "CLIENTE": {"rich_text": [{"text": {"content": cli}}]},
                "DT SAÍDA": {"date": {"start": dt_s.strftime('%Y-%m-%d')}},
                "INÍCIO DA MISSÃO": {"date": {"start": ini.strftime('%Y-%m-%d')}},
                "FIM DA MISSÃO": {"date": {"start": fim.strftime('%Y-%m-%d')}},
                "EMPURRADOR": {"rich_text": [{"text": {"content": emp}}]},
                "BALSA": {"rich_text": [{"text": {"content": bal}}]},
                "LOCAL": {"rich_text": [{"text": {"content": loc}}]},
                "DESTINO": {"rich_text": [{"text": {"content": dest}}]},
                "HORA DE EMBARQUE": {"rich_text": [{"text": {"content": h_emb}}]},
                "ESCOLTA 1": {"rich_text": [{"text": {"content": esc1}}]},
                "ESCOLTA 2": {"rich_text": [{"text": {"content": esc2}}]},
                "PEDIDO": {"rich_text": [{"text": {"content": ped}}]},
                "ASSINATURA RESPONSÁVEL": {"rich_text": [{"text": {"content": ass}}]},
                "DESCRIÇÃO": {"rich_text": [{"text": {"content": obs}}]},
                "STATUS": {"select": {"name": sts}}
            }}
            
            url = f"https://api.notion.com/v1/pages/{edit['ID']}" if edit else "https://api.notion.com/v1/pages"
            if not edit: payload["parent"] = {"database_id": DATABASE}
            res = requests.patch(url, headers=headers, json=payload) if edit else requests.post(url, headers=headers, json=payload)
            
            if res.status_code == 200:
                st.success("🎯 Sucesso! Redirecionando...")
                navegar("📊 GRADE")
            else:
                st.error(f"Erro no Notion: {res.text}")

# --- TELA GRADE (AÇÕES DIRETAS) ---
elif st.session_state.pagina == "📊 GRADE":
    if st.button("⬅️ VOLTAR PARA HOME"): navegar("🏠 HOME")
    st.subheader("📊 Agendamentos e O.S Ativas")
    dados = carregar_dados_notion()
    if dados:
        df = pd.DataFrame(dados)
        st.dataframe(df[["Nº OS", "CLIENTE", "DT SAÍDA", "STATUS"]], use_container_width=True)
        
        for d in dados:
            with st.expander(f"🛠️ AÇÕES: O.S {d['Nº OS']} - {d['CLIENTE']}"):
                col1, col2 = st.columns(2)
                if col1.button("✏️ EDITAR", key=f"edit_{d['ID']}"):
                    st.session_state.dados_edicao = d; navegar("📋 CADASTRO")
                
                pdf_output = gerar_pdf_transdourada(d)
                col2.download_button("📄 GERAR PDF O.S", pdf_output, f"OS_{d['Nº OS']}.pdf", key=f"pdf_{d['ID']}")
    else:
        st.info("Nenhum agendamento encontrado.")

# --- TELA FINANCEIRO ---
elif st.session_state.pagina == "💰 FINANCEIRO":
    if st.button("⬅️ VOLTAR"): navegar("🏠 HOME")
    st.header("💰 Resumo Operacional / Financeiro")
    dados = carregar_dados_notion()
    if dados:
        df = pd.DataFrame(dados)
        c1, c2 = st.columns(2)
        c1.metric("O.S EM ABERTO", len(df[df['STATUS'] == "Em Andamento"]))
        c2.metric("O.S ENCERRADAS", len(df[df['STATUS'] == "Encerrado"]))
        st.table(df[["Nº OS", "CLIENTE", "STATUS", "DT SAÍDA"]])
