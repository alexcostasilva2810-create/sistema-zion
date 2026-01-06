import streamlit as st
import requests
import pandas as pd
import os
from fpdf import FPDF
from datetime import datetime

# 1. CONFIGURAÇÃO DA PÁGINA (LOGO E TÍTULO)
st.set_page_config(page_title="Zion Tecnologia", layout="wide")

# --- CONEXÃO NOTION ---
# Verifique se no seu Secrets os nomes estão exatamente assim: token e database_id
TOKEN = st.secrets["notion"]["token"].replace('"', '').strip()
DATABASE = st.secrets["notion"]["database_id"].replace('"', '').strip()

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

# --- ESTILO VISUAL ---
st.markdown("""
    <style>
    div.stButton > button:first-child[kind="primary"] { background-color: #28a745 !important; color: white !important; }
    .stButton>button { width: 100%; border-radius: 8px; font-weight: bold; height: 3.5em; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNÇÃO PDF (ESTILO TRANSDOURADA - ANEXO 2) ---
def gerar_pdf_final(d):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 5, "TRANSDOURADA NAVEGAÇÃO LTDA", ln=True)
    pdf.set_font("Arial", "", 8)
    pdf.cell(0, 5, "SISTEMA ZION - PVH SEG", ln=True)
    pdf.ln(10)

    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "ORDEM DE SERVIÇO", ln=True, align="C")
    pdf.set_font("Arial", "B", 11)
    pdf.cell(0, 10, f"SOLICITANTE: {d.get('CLIENTE', '---').upper()}", border=1, ln=True, align="C", fill=False)
    
    pdf.set_font("Arial", "", 9)
    # Linhas de Dados Técnicos
    pdf.cell(95, 8, f"O.S Nº: {d.get('Nº OS', '---')}", border=1)
    pdf.cell(95, 8, f"PEDIDO: {d.get('PEDIDO', '---')}", border=1, ln=True)
    pdf.cell(95, 8, f"EMPURRADOR: {d.get('EMPURRADOR', '---')}", border=1)
    pdf.cell(95, 8, f"BALSA: {d.get('BALSA', '---')}", border=1, ln=True)
    pdf.cell(95, 8, f"ORIGEM: {d.get('LOCAL', '---')}", border=1)
    pdf.cell(95, 8, f"DESTINO: {d.get('DESTINO', '---')}", border=1, ln=True)
    pdf.cell(95, 8, f"INÍCIO MISSÃO: {d.get('INÍCIO', '---')}", border=1)
    pdf.cell(95, 8, f"FIM MISSÃO: {d.get('FIM', '---')}", border=1, ln=True)
    pdf.cell(95, 8, f"ESCOLTA 1: {d.get('ESCOLTA 1', '---')}", border=1)
    pdf.cell(95, 8, f"ESCOLTA 2: {d.get('ESCOLTA 2', '---')}", border=1, ln=True)
    
    pdf.ln(5)
    pdf.set_font("Arial", "B", 10)
    pdf.cell(0, 8, "DESCRIÇÃO DOS SERVIÇOS:", ln=True)
    pdf.set_font("Arial", "", 10)
    pdf.multi_cell(0, 6, d.get('DESCRIÇÃO', '---'), border=1)
    
    pdf.ln(15)
    pdf.cell(95, 7, "__________________________", ln=0, align="C")
    pdf.cell(95, 7, "__________________________", ln=1, align="C")
    pdf.cell(95, 7, f"{d.get('ASSINATURA', 'Responsável')}", ln=0, align="C")
    pdf.cell(95, 7, "Zion / Fiscalização", ln=1, align="C")

    return pdf.output(dest="S").encode("latin-1")

# --- FUNÇÃO CARREGAR (ROBUSTA) ---
def carregar_dados():
    try:
        res = requests.post(f"https://api.notion.com/v1/databases/{DATABASE}/query", headers=headers)
        if res.status_code == 200:
            results = res.json().get("results", [])
            lista = []
            for r in results:
                p = r["properties"]
                # Função interna para evitar quebra se campo for vazio
                def txt(n): 
                    try: return p[n]["rich_text"][0]["plain_text"]
                    except: return "---"
                def dat(n):
                    try: return datetime.strptime(p[n]["date"]["start"], '%Y-%m-%d').strftime('%d/%m/%Y')
                    except: return "---"

                lista.append({
                    "ID": r["id"],
                    "Nº OS": p["Nº OS"]["title"][0]["plain_text"] if p["Nº OS"]["title"] else "---",
                    "CLIENTE": txt("CLIENTE"), "DT SAÍDA": dat("DT SAÍDA"),
                    "EMPURRADOR": txt("EMPURRADOR"), "BALSA": txt("BALSA"),
                    "LOCAL": txt("LOCAL"), "DESTINO": txt("DESTINO"),
                    "HORA_EMBARQUE": txt("HORA DE EMBARQUE"),
                    "ESCOLTA 1": txt("ESCOLTA 1"), "ESCOLTA 2": txt("ESCOLTA 2"),
                    "DESCRIÇÃO": txt("DESCRIÇÃO"), "PEDIDO": txt("PEDIDO"),
                    "INÍCIO": dat("INÍCIO DA MISSÃO"), "FIM": dat("FIM DA MISSÃO"),
                    "ASSINATURA": txt("ASSINATURA RESPONSÁVEL"),
                    "STATUS": p["STATUS"]["select"]["name"] if p["STATUS"]["select"] else "---"
                })
            return lista
    except: return []

# --- NAVEGAÇÃO ---
if "pagina" not in st.session_state: st.session_state.pagina = "🏠 HOME"
if "dados_edicao" not in st.session_state: st.session_state.dados_edicao = None
def navegar(p): st.session_state.pagina = p; st.rerun()

# --- TELAS ---
if st.session_state.pagina == "🏠 HOME":
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Zion_National_Park_logo.svg/1200px-Zion_National_Park_logo.svg.png", width=150) # Logo Zion
    st.title("🛡️ Zion Gestão Transdourada")
    c1, c2 = st.columns(2)
    if c1.button("📋 NOVO LANÇAMENTO"): st.session_state.dados_edicao = None; navegar("📋 CADASTRO")
    if c2.button("📊 VER AGENDAMENTOS"): navegar("📊 GRADE")

elif st.session_state.pagina == "📋 CADASTRO":
    edit = st.session_state.dados_edicao
    st.header("📝 Formulário de O.S")
    if st.button("⬅️ VOLTAR"): navegar("🏠 HOME")
    
    with st.form("f_os"):
        c1, c2, c3 = st.columns(3)
        os_n = c1.text_input("Nº O.S", value=edit["Nº OS"] if edit else "")
        dt_s = c2.date_input("DATA SAÍDA")
        cli = c3.text_input("CLIENTE", value=edit["CLIENTE"] if edit else "")
        
        c4, c5, c6 = st.columns(3)
        emp = c4.text_input("EMPURRADOR", value=edit["EMPURRADOR"] if edit else "")
        bal = c5.text_input("BALSA", value=edit["BALSA"] if edit else "")
        ped = c6.text_input("PEDIDO", value=edit["PEDIDO"] if edit else "")
        
        c7, c8, c9 = st.columns(3)
        loc = c7.text_input("LOCAL/ORIGEM", value=edit["LOCAL"] if edit else "")
        dst = c8.text_input("DESTINO", value=edit["DESTINO"] if edit else "")
        h_e = c9.text_input("HORA EMBARQUE", value=edit["HORA_EMBARQUE"] if edit else "")
        
        c10, c11, c12 = st.columns(3)
        es1 = c10.text_input("ESCOLTA 1", value=edit["ESCOLTA 1"] if edit else "")
        es2 = c11.text_input("ESCOLTA 2", value=edit["ESCOLTA 2"] if edit else "")
        ass = c12.text_input("ASSINATURA", value=edit["ASSINATURA"] if edit else "")

        obs = st.text_area("DESCRIÇÃO", value=edit["DESCRIÇÃO"] if edit else "")
        sts = st.selectbox("STATUS", ["Em Andamento", "Encerrado"])
        
        if st.form_submit_button("✅ SALVAR OPERAÇÃO", type="primary"):
            payload = {"properties": {
                "Nº OS": {"title": [{"text": {"content": str(os_n)}}]},
                "CLIENTE": {"rich_text": [{"text": {"content": cli}}]},
                "DT SAÍDA": {"date": {"start": dt_s.strftime('%Y-%m-%d')}},
                "EMPURRADOR": {"rich_text": [{"text": {"content": emp}}]},
                "BALSA": {"rich_text": [{"text": {"content": bal}}]},
                "LOCAL": {"rich_text": [{"text": {"content": loc}}]},
                "DESTINO": {"rich_text": [{"text": {"content": dst}}]},
                "HORA DE EMBARQUE": {"rich_text": [{"text": {"content": h_e}}]},
                "ESCOLTA 1": {"rich_text": [{"text": {"content": es1}}]},
                "ESCOLTA 2": {"rich_text": [{"text": {"content": es2}}]},
                "PEDIDO": {"rich_text": [{"text": {"content": ped}}]},
                "ASSINATURA RESPONSÁVEL": {"rich_text": [{"text": {"content": ass}}]},
                "DESCRIÇÃO": {"rich_text": [{"text": {"content": obs}}]},
                "STATUS": {"select": {"name": sts}}
            }}
            url = f"https://api.notion.com/v1/pages/{edit['ID']}" if edit else "https://api.notion.com/v1/pages"
            if not edit: payload["parent"] = {"database_id": DATABASE}
            res = requests.patch(url, headers=headers, json=payload) if edit else requests.post(url, headers=headers, json=payload)
            if res.status_code == 200:
                st.success("Salvo!"); navegar("📊 GRADE")
            else: st.error(f"Erro: {res.text}")

elif st.session_state.pagina == "📊 GRADE":
    st.header("📊 Agendamentos Ativos")
    if st.button("⬅️ VOLTAR"): navegar("🏠 HOME")
    dados = carregar_dados()
    if dados:
        df = pd.DataFrame(dados)
        st.dataframe(df[["Nº OS", "CLIENTE", "STATUS"]], use_container_width=True)
        for d in dados:
            with st.expander(f"⚙️ O.S {d['Nº OS']} - {d['CLIENTE']}"):
                c1, c2 = st.columns(2)
                if c1.button("✏️ EDITAR", key=f"ed_{d['ID']}"):
                    st.session_state.dados_edicao = d; navegar("📋 CADASTRO")
                pdf_b = gerar_pdf_final(d)
                c2.download_button("📄 PDF O.S", pdf_b, f"OS_{d['Nº OS']}.pdf", key=f"pdf_{d['ID']}")
