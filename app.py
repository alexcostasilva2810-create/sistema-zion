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
    div.stButton > button:first-child[kind="primary"] { background-color: #28a745; color: white; border: none; }
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
    pdf.cell(0, 10, f"SOLICITANTE ( {d.get('CLIENTE', '---').upper()} )", border=1, ln=True, align="C")
    pdf.ln(5)
    pdf.set_font("Arial", "", 10)
    pdf.multi_cell(0, 6, f"DESCRIÇÃO: {d.get('DESCRIÇÃO', '---')}")
    pdf.set_y(-35)
    pdf.set_font("Arial", "B", 7)
    pdf.cell(0, 5, "TRANSDOURADA NAVEGAÇÃO LTDA - ANANINDEUA/PA", ln=True, align="C")
    return pdf.output(dest="S").encode("latin-1")

# --- FUNÇÃO PUXAR DADOS DO NOTION ---
def carregar_dados_notion():
    try:
        url = f"https://api.notion.com/v1/databases/{DATABASE}/query"
        res = requests.post(url, headers=headers)
        if res.status_code == 200:
            results = res.json().get("results", [])
            lista = []
            for r in results:
                p = r["properties"]
                # Convertendo datas do Notion para formato BR na visualização
                def fmt_data(campo):
                    dt = p.get(campo, {}).get("date", {}).get("start")
                    return datetime.strptime(dt, '%Y-%m-%d').strftime('%d/%m/%Y') if dt else "---"

                lista.append({
                    "ID_NOTION": r["id"],
                    "Nº OS": p["Nº OS"]["title"][0]["plain_text"] if p["Nº OS"]["title"] else "---",
                    "CLIENTE": p["CLIENTE"]["rich_text"][0]["plain_text"] if p["CLIENTE"]["rich_text"] else "---",
                    "DT SAÍDA": fmt_data("DT SAÍDA"),
                    "INÍCIO": fmt_data("INÍCIO DA MISSÃO"),
                    "FIM": fmt_data("FIM DA MISSÃO"),
                    "EMPURRADOR": p["EMPURRADOR"]["rich_text"][0]["plain_text"] if p["EMPURRADOR"]["rich_text"] else "---",
                    "STATUS": p["STATUS"]["select"]["name"] if p["STATUS"]["select"] else "---",
                    "BALSA": p["BALSA"]["rich_text"][0]["plain_text"] if p["BALSA"]["rich_text"] else "---",
                    "DESCRIÇÃO": p["DESCRIÇÃO"]["rich_text"][0]["plain_text"] if p["DESCRIÇÃO"]["rich_text"] else "---",
                    "SERVIÇO": p["SERVIÇO"]["select"]["name"] if p["SERVIÇO"]["select"] else "---"
                })
            return lista
    except: return []
    return []

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

# --- TELA DE CADASTRO (17 CAMPOS COM DATA BR) ---
elif st.session_state.pagina == "📋 CADASTRO":
    edit = st.session_state.dados_edicao
    if st.button("⬅️ VOLTAR"): navegar("🏠 HOME")
    st.header("📝 Cadastro de Missão")
    
    with st.form("form_missao"):
        c1, c2, c3 = st.columns(3)
        os_n = c1.text_input("Nº O.S", value=edit["Nº OS"] if edit else "")
        # FORMATO BR NO CALENDÁRIO
        dt_saida = c2.date_input("DT SAÍDA", format="DD/MM/YYYY") 
        cliente = c3.text_input("CLIENTE", value=edit["CLIENTE"] if edit else "")
        
        c4, c5, c6 = st.columns(3)
        ini_m = c4.date_input("INÍCIO DA MISSÃO", format="DD/MM/YYYY")
        fim_m = c5.date_input("FIM DA MISSÃO", format="DD/MM/YYYY")
        balsa = c6.text_input("BALSA", value=edit["BALSA"] if edit else "")
        
        c7, c8, c9 = st.columns(3)
        h_emb = c7.text_input("HORA DE EMBARQUE")
        esc1 = c8.text_input("ESCOLTA 1")
        destino = c9.text_input("DESTINO")
        
        c10, c11, c12 = st.columns(3)
        local = c10.text_input("LOCAL")
        esc2 = c11.text_input("ESCOLTA 2")
        pedido = c12.text_input("PEDIDO")
        
        c13, c14, c15 = st.columns(3)
        empurrador = c13.text_input("EMPURRADOR", value=edit["EMPURRADOR"] if edit else "")
        servico = c14.selectbox("SERVIÇO", ["Escolta", "Vigilância"])
        ass_resp = c15.text_input("ASSINATURA RESPONSÁVEL")
        
        desc = st.text_area("DESCRIÇÃO / OBSERVAÇÕES", value=edit["DESCRIÇÃO"] if edit else "")
        status = st.selectbox("STATUS", ["Em Andamento", "Encerrado"])
        
        if st.form_submit_button("✅ SALVAR OPERAÇÃO", type="primary"):
            # Envio para o Notion (O Notion exige YYYY-MM-DD internamente)
            payload = {
                "parent": {"database_id": DATABASE} if not edit else None,
                "properties": {
                    "Nº OS": {"title": [{"text": {"content": os_n}}]},
                    "CLIENTE": {"rich_text": [{"text": {"content": cliente}}]},
                    "DT SAÍDA": {"date": {"start": dt_saida.strftime('%Y-%m-%d')}},
                    "INÍCIO DA MISSÃO": {"date": {"start": ini_m.strftime('%Y-%m-%d')}},
                    "STATUS": {"select": {"name": status}},
                    "EMPURRADOR": {"rich_text": [{"text": {"content": empurrador}}]},
                    "DESCRIÇÃO": {"rich_text": [{"text": {"content": desc}}]}
                }
            }
            url = f"https://api.notion.com/v1/pages/{edit['ID_NOTION']}" if edit else "https://api.notion.com/v1/pages"
            res = requests.patch(url, headers=headers, json={"properties": payload["properties"]}) if edit else requests.post(url, headers=headers, json=payload)
            
            if res.status_code == 200:
                st.success("🎯 Sucesso!"); navegar("🏠 HOME")
            else: st.error(f"Erro no Notion: {res.text}")

# --- TELA GRADE ---
elif st.session_state.pagina == "📊 GRADE":
    if st.button("⬅️ VOLTAR"): navegar("🏠 HOME")
    st.subheader("📊 Agendamentos")
    dados = carregar_dados_notion()
    if dados:
        for d in dados:
            with st.expander(f"O.S: {d['Nº OS']} - {d['CLIENTE']} ({d['DT SAÍDA']})"):
                c_a, c_b = st.columns([3, 1])
                c_a.write(f"**Empurrador:** {d['EMPURRADOR']} | **Status:** {d['STATUS']}")
                if c_b.button("✏️ Editar", key=f"ed_{d['ID_NOTION']}"):
                    st.session_state.dados_edicao = d
                    navegar("📋 CADASTRO")
                pdf_b = gerar_pdf_transdourada(d)
                c_b.download_button("📄 PDF", pdf_b, f"OS_{d['Nº OS']}.pdf", key=f"pdf_{d['ID_NOTION']}")

# --- TELA FINANCEIRO ---
elif st.session_state.pagina == "💰 FINANCEIRO":
    if st.button("⬅️ VOLTAR"): navegar("🏠 HOME")
    st.header("💰 Financeiro")
    st.table(pd.DataFrame(columns=["DATA", "PEDIDO", "VALOR", "STATUS"]))
