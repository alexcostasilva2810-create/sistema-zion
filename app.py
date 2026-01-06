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

# --- ESTILO CSS ---
st.markdown("""
    <style>
    div.stButton > button:first-child[kind="primary"] { background-color: #28a745 !important; color: white !important; }
    .stButton>button { width: 100%; border-radius: 8px; font-weight: bold; height: 3.5em; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNÇÃO GERAR PDF MODELO TRANSDOURADA (FANTÁSTICO) ---
def gerar_pdf_transdourada(d):
    pdf = FPDF()
    pdf.add_page()
    
    # Cabeçalho com Logos (Referência ao Anexo 2)
    # Se você tiver o arquivo da logo no servidor, pode usar pdf.image("logo.png", 10, 8, 33)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 5, "TRANSDOURADA", ln=True, align="L")
    pdf.set_font("Arial", "", 8)
    pdf.cell(0, 5, "Navegação Ltda.    GRUPO DIAS", ln=True, align="L")
    pdf.ln(10)

    # Título Centralizado
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Solicitação de Escolta", ln=True, align="C")
    pdf.set_font("Arial", "B", 10)
    pdf.cell(0, 6, "ORDEM DE SERVIÇO", ln=True, align="C")
    pdf.cell(0, 6, f"O.S: {d.get('Nº OS', '---')}", ln=True, align="C")
    pdf.set_font("Arial", "B", 9)
    pdf.cell(0, 6, f"STATUS: {d.get('STATUS', '---').upper()}", ln=True, align="C")
    pdf.ln(4)

    # QUADRO SOLICITANTE
    pdf.set_font("Arial", "B", 11)
    pdf.cell(0, 10, f"SOLICITANTE ( {d.get('CLIENTE', '---').upper()} )", border=1, ln=True, align="C")
    pdf.ln(5)

    # BLOCO DE DADOS TÉCNICOS (GRID)
    pdf.set_font("Arial", "", 10)
    # Linha 1
    pdf.cell(95, 8, f"EMPURRADOR: {d.get('EMPURRADOR', '---')}", border="LT")
    pdf.cell(95, 8, f"SAÍDA PREVISTA: {d.get('HORA_EMBARQUE', '---')}", border="RT", ln=True)
    # Linha 2
    pdf.cell(95, 8, f"ORIGEM: {d.get('LOCAL', '---')}", border="L")
    pdf.cell(95, 8, f"DESTINO: {d.get('DESTINO', '---')}", border="R", ln=True)
    # Linha 3
    pdf.cell(95, 8, f"BALSA: {d.get('BALSA', '---')}", border="LB")
    pdf.cell(95, 8, f"SERVIÇO: {d.get('SERVIÇO', '---')}", border="RB", ln=True)
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
    pdf.cell(0, 10, "DETALHAMENTO DA MISSÃO.", border="T", ln=True, align="C")
    pdf.ln(2)
    
    # TEXTO DA DESCRIÇÃO
    pdf.set_font("Arial", "", 10)
    pdf.multi_cell(0, 6, f"DESCRIÇÃO: {d.get('DESCRIÇÃO', '---')}")

    # RODAPÉ
    pdf.set_y(-30)
    pdf.set_font("Arial", "", 7)
    pdf.cell(0, 4, "TRANSDOURADA NAVEGAÇÃO LTDA 01.259.730/0001-74", ln=True, align="C")
    pdf.cell(0, 4, "ROD BR 316 KM 08, SN AGUA BRANCA 67033-070 ANANINDEUA", ln=True, align="C")

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
                    "Nº OS": p["Nº OS"]["title"][0]["plain_text"] if "Nº OS" in p and p["Nº OS"]["title"] else "---",
                    "CLIENTE": g_t("CLIENTE"), "DT SAÍDA": g_d("DT SAÍDA"),
                    "INÍCIO": g_d("INÍCIO DA MISSÃO"), "FIM": g_d("FIM DA MISSÃO"),
                    "EMPURRADOR": g_t("EMPURRADOR"), "BALSA": g_t("BALSA"),
                    "LOCAL": g_t("LOCAL"), "DESTINO": g_t("DESTINO"),
                    "HORA_EMBARQUE": g_t("HORA DE EMBARQUE"),
                    "ESCOLTA 1": g_t("ESCOLTA 1"), "ESCOLTA 2": g_t("ESCOLTA 2"),
                    "DESCRIÇÃO": g_t("DESCRIÇÃO"), "ASSINATURA": g_t("ASSINATURA RESPONSÁVEL"),
                    "PEDIDO": g_t("PEDIDO"),
                    "SERVIÇO": p["SERVIÇO"]["select"]["name"] if "SERVIÇO" in p and p["SERVIÇO"]["select"] else "---",
                    "STATUS": p["STATUS"]["select"]["name"] if "STATUS" in p and p["STATUS"]["select"] else "---"
                })
            return lista
    except: return []
    return []

# --- NAVEGAÇÃO ---
if "pagina" not in st.session_state: st.session_state.pagina = "🏠 HOME"
if "dados_edicao" not in st.session_state: st.session_state.dados_edicao = None

def navegar(p): st.session_state.pagina = p; st.rerun()

# --- TELAS ---
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

elif st.session_state.pagina == "📋 CADASTRO":
    edit = st.session_state.dados_edicao
    if st.button("⬅️ VOLTAR"): navegar("🏠 HOME")
    st.header("📝 Lançamento de O.S")
    with st.form("form_completo"):
        c1, c2, c3 = st.columns(3)
        os_n = c1.text_input("Nº O.S", value=edit["Nº OS"] if edit else "")
        dt_s = c2.date_input("DT SAÍDA", format="DD/MM/YYYY")
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
        loc = c10.text_input("LOCAL", value=edit.get("LOCAL", "") if edit else "")
        esc2 = c11.text_input("ESCOLTA 2", value=edit.get("ESCOLTA 2", "") if edit else "")
        ped = c12.text_input("PEDIDO", value=edit.get("PEDIDO", "") if edit else "")
        
        c13, c14, c15 = st.columns(3)
        emp = c13.text_input("EMPURRADOR", value=edit.get("EMPURRADOR", "") if edit else "")
        ser = c14.selectbox("SERVIÇO", ["Escolta", "Vigilância"])
        ass = c15.text_input("ASSINATURA RESPONSÁVEL", value=edit.get("ASSINATURA", "") if edit else "")
        
        obs = st.text_area("DESCRIÇÃO / OBSERVAÇÕES", value=edit.get("DESCRIÇÃO", "") if edit else "")
        sts = st.selectbox("STATUS", ["Em Andamento", "Encerrado"])
        
        if st.form_submit_button("✅ SALVAR OPERAÇÃO", type="primary"):
            payload = {"properties": {
                "Nº OS": {"title": [{"text": {"content": os_n}}]},
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
                "SERVIÇO": {"select": {"name": ser}},
                "STATUS": {"select": {"name": sts}}
            }}
            url = f"https://api.notion.com/v1/pages/{edit['ID']}" if edit else "https://api.notion.com/v1/pages"
            if not edit: payload["parent"] = {"database_id": DATABASE}
            res = requests.patch(url, headers=headers, json=payload) if edit else requests.post(url, headers=headers, json=payload)
            if res.status_code == 200:
                st.success("Salvo!"); navegar("🏠 HOME")

elif st.session_state.pagina == "📊 GRADE":
    if st.button("⬅️ VOLTAR"): navegar("🏠 HOME")
    st.subheader("📊 Agendamentos Ativos")
    dados = carregar_dados_notion()
    if dados:
        df_visual = pd.DataFrame(dados)
        st.dataframe(df_visual[["Nº OS", "CLIENTE", "DT SAÍDA", "STATUS"]], use_container_width=True)
        for d in dados:
            with st.expander(f"⚙️ O.S {d['Nº OS']} - {d['CLIENTE']}"):
                c1, c2 = st.columns(2)
                if c1.button("✏️ Editar Registro", key=f"e_{d['ID']}"):
                    st.session_state.dados_edicao = d; navegar("📋 CADASTRO")
                pdf_file = gerar_pdf_transdourada(d)
                c2.download_button("📄 Imprimir O.S", pdf_file, f"OS_{d['Nº OS']}.pdf", key=f"p_{d['ID']}")

elif st.session_state.pagina == "💰 FINANCEIRO":
    if st.button("⬅️ VOLTAR"): navegar("🏠 HOME")
    dados = carregar_dados_notion()
    if dados:
        df = pd.DataFrame(dados)
        c1, c2 = st.columns(2)
        c1.metric("O.S ABERTAS", len(df[df['STATUS'] == "Em Andamento"]))
        c2.metric("O.S ENCERRADAS", len(df[df['STATUS'] == "Encerrado"]))
        st.table(df[["Nº OS", "CLIENTE", "STATUS"]])
