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

# --- ESTILO CSS (BOTÃO SALVAR VERDE E DESIGN) ---
st.markdown("""
    <style>
    /* Botão Salvar Verde */
    div.stButton > button:first-child[kind="primary"] {
        background-color: #28a745;
        color: white;
        border: none;
    }
    /* Botão Geral Zion */
    .stButton>button { width: 100%; border-radius: 8px; font-weight: bold; height: 3.5em; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNÇÃO GERAR PDF (IDÊNTICO AO MODELO TRANSDOURADA) ---
def gerar_pdf_transdourada(d):
    pdf = FPDF()
    pdf.add_page()
    
    # Logo e Cabeçalho (Simulado com texto conforme imagem)
    pdf.set_font("Arial", "B", 10)
    pdf.cell(0, 5, "ZION TECNOLOGIA | TRANSDOURADA", ln=True)
    pdf.set_font("Arial", "", 8)
    pdf.cell(0, 5, "Navegação Ltda.    GRUPO DIAS", ln=True)
    pdf.ln(10)

    # Título Central
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Solicitação de Escolta", ln=True, align="C")
    pdf.set_font("Arial", "B", 11)
    pdf.cell(0, 7, "ORDEM DE SERVIÇO", ln=True, align="C")
    pdf.cell(0, 7, f"O.S: {d.get('Nº OS', '---')}", ln=True, align="C")
    pdf.set_font("Arial", "", 10)
    pdf.cell(0, 7, f"STATUS: {d.get('STATUS', '---').upper()}", ln=True, align="C")
    pdf.ln(2)

    # Caixa Solicitante
    pdf.set_font("Arial", "B", 11)
    pdf.cell(0, 10, f"SOLICITANTE ( {d.get('CLIENTE', '---').upper()} )", border=1, ln=True, align="C")
    pdf.ln(5)

    # Grid Técnico
    pdf.set_font("Arial", "", 9)
    y_start = pdf.get_y()
    pdf.text(10, y_start, f"EMPURRADOR: {d.get('EMPURRADOR', '---')}")
    pdf.text(80, y_start, f"SAÍDA PREVISTA: {d.get('HORA_EMBARQUE', '---')}")
    pdf.text(150, y_start, f"STATUS: {d.get('STATUS', '---')}")
    
    pdf.text(10, y_start+6, f"ORIGEM: {d.get('LOCAL', '---')}")
    pdf.text(80, y_start+6, f"DESTINO: {d.get('DESTINO', '---')}")
    pdf.text(150, y_start+6, f"SERVIÇO: {d.get('SERVIÇO', '---')}")
    
    pdf.text(10, y_start+12, f"BALSA: {d.get('BALSA', '---')}")
    pdf.ln(20)

    # Caixa PVH-SEG
    pdf.set_font("Arial", "B", 11)
    pdf.cell(0, 10, "PVH-SEG Serv. de Vig. Patrimonial Ltda", border=1, ln=True, align="C")
    pdf.ln(5)

    # Datas da Missão
    pdf.set_font("Arial", "", 10)
    pdf.cell(0, 6, f"INÍCIO DA MISSÃO: {d.get('INÍCIO', '---')}", ln=True)
    pdf.cell(0, 6, f"ESCOLTA 1: {d.get('ESCOLTA 1', '---')}", ln=True)
    pdf.cell(0, 6, f"ESCOLTA 2: {d.get('ESCOLTA 2', '---')}", ln=True)
    pdf.cell(0, 6, f"FIM DA MISSÃO: {d.get('DT SAÍDA', '---')}", ln=True)
    
    pdf.ln(10)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "DETALHAMENTO DA MISSÃO.", ln=True, align="C")
    pdf.set_font("Arial", "", 10)
    pdf.multi_cell(0, 6, f"DESCRIÇÃO: {d.get('DESCRIÇÃO', '---')}")

    # Rodapé
    pdf.set_y(-35)
    pdf.cell(190, 0, "", border="T", ln=True)
    pdf.set_font("Arial", "B", 7)
    pdf.cell(0, 5, "TRANSDOURADA NAVEGAÇÃO LTDA - 01.269.730/0001-74", ln=True, align="C")
    pdf.cell(0, 5, "ROD BR 316 KM 08, SN ÁGUA BRANCA - ANANINDEUA/PA", ln=True, align="C")

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
                lista.append({
                    "ID_NOTION": r["id"],
                    "Nº OS": p["Nº OS"]["title"][0]["plain_text"] if p["Nº OS"]["title"] else "---",
                    "CLIENTE": p["CLIENTE"]["rich_text"][0]["plain_text"] if p["CLIENTE"]["rich_text"] else "---",
                    "DT SAÍDA": p["DT SAÍDA"]["date"]["start"] if p["DT SAÍDA"]["date"] else "---",
                    "INÍCIO": p["INÍCIO DA MISSÃO"]["date"]["start"] if p["INÍCIO DA MISSÃO"]["date"] else "---",
                    "EMPURRADOR": p["EMPURRADOR"]["rich_text"][0]["plain_text"] if p["EMPURRADOR"]["rich_text"] else "---",
                    "STATUS": p["STATUS"]["select"]["name"] if p["STATUS"]["select"] else "---",
                    "BALSA": p["BALSA"]["rich_text"][0]["plain_text"] if p["BALSA"]["rich_text"] else "---",
                    "DESCRIÇÃO": p["DESCRIÇÃO"]["rich_text"][0]["plain_text"] if p["DESCRIÇÃO"]["rich_text"] else "---",
                    "SERVIÇO": p["SERVIÇO"]["select"]["name"] if p["SERVIÇO"]["select"] else "---",
                    "ESCOLTA 1": p.get("ESCOLTA 1", {}).get("rich_text", [{}])[0].get("plain_text", "---"),
                    "ESCOLTA 2": p.get("ESCOLTA 2", {}).get("rich_text", [{}])[0].get("plain_text", "---"),
                    "LOCAL": p.get("LOCAL", {}).get("rich_text", [{}])[0].get("plain_text", "---"),
                    "DESTINO": p.get("DESTINO", {}).get("rich_text", [{}])[0].get("plain_text", "---"),
                    "HORA_EMBARQUE": p.get("HORA DE EMBARQUE", {}).get("rich_text", [{}])[0].get("plain_text", "---")
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
        if st.button("📋 NOVO LANÇAMENTO"): 
            st.session_state.dados_edicao = None
            navegar("📋 CADASTRO")
    with c2: 
        if st.button("📊 VER AGENDAMENTOS"): navegar("📊 GRADE")
    with c3: 
        if st.button("💰 FINANCEIRO"): navegar("💰 FINANCEIRO")

# --- TELA DE CADASTRO / EDIÇÃO (17 CAMPOS) ---
elif st.session_state.pagina == "📋 CADASTRO":
    edit = st.session_state.dados_edicao
    titulo = "📝 Editar Missão" if edit else "📝 Novo Lançamento"
    if st.button("⬅️ VOLTAR"): navegar("🏠 HOME")
    st.header(titulo)
    
    with st.form("form_missao"):
        c1, c2, c3 = st.columns(3)
        os_n = c1.text_input("Nº O.S", value=edit["Nº OS"] if edit else "")
        dt_saida = c2.date_input("DT SAÍDA", value=datetime.strptime(edit["DT SAÍDA"], '%Y-%m-%d') if edit and edit["DT SAÍDA"] != "---" else datetime.today())
        cliente = c3.text_input("CLIENTE", value=edit["CLIENTE"] if edit else "")
        
        c4, c5, c6 = st.columns(3)
        ini_m = c4.date_input("INÍCIO DA MISSÃO", value=datetime.strptime(edit["INÍCIO"], '%Y-%m-%d') if edit and edit["INÍCIO"] != "---" else datetime.today())
        fim_m = c5.date_input("FIM DA MISSÃO")
        balsa = c6.text_input("BALSA", value=edit["BALSA"] if edit else "")
        
        c7, c8, c9 = st.columns(3)
        h_emb = c7.text_input("HORA DE EMBARQUE", value=edit.get("HORA_EMBARQUE", "") if edit else "")
        esc1 = c8.text_input("ESCOLTA 1", value=edit.get("ESCOLTA 1", "") if edit else "")
        destino = c9.text_input("DESTINO", value=edit.get("DESTINO", "") if edit else "")
        
        c10, c11, c12 = st.columns(3)
        local = c10.text_input("LOCAL", value=edit.get("LOCAL", "") if edit else "")
        esc2 = c11.text_input("ESCOLTA 2", value=edit.get("ESCOLTA 2", "") if edit else "")
        pedido = c12.text_input("PEDIDO")
        
        c13, c14, c15 = st.columns(3)
        empurrador = c13.text_input("EMPURRADOR", value=edit["EMPURRADOR"] if edit else "")
        servico = c14.selectbox("SERVIÇO", ["Escolta", "Vigilância"])
        ass_resp = c15.text_input("ASSINATURA RESPONSÁVEL")
        
        desc = st.text_area("DESCRIÇÃO / OBSERVAÇÕES", value=edit["DESCRIÇÃO"] if edit else "")
        status = st.selectbox("STATUS", ["Em Andamento", "Encerrado", "Cancelado"])
        
        # BOTÃO SALVAR VERDE
        if st.form_submit_button("✅ SALVAR OPERAÇÃO", type="primary"):
            payload = {
                "parent": {"database_id": DATABASE} if not edit else None,
                "properties": {
                    "Nº OS": {"title": [{"text": {"content": os_n}}]},
                    "CLIENTE": {"rich_text": [{"text": {"content": cliente}}]},
                    "DT SAÍDA": {"date": {"start": str(dt_saida)}},
                    "STATUS": {"select": {"name": status}},
                    "EMPURRADOR": {"rich_text": [{"text": {"content": empurrador}}]},
                    "DESCRIÇÃO": {"rich_text": [{"text": {"content": desc}}]},
                    "INÍCIO DA MISSÃO": {"date": {"start": str(ini_m)}}
                }
            }
            if edit:
                url = f"https://api.notion.com/v1/pages/{edit['ID_NOTION']}"
                res = requests.patch(url, headers=headers, json={"properties": payload["properties"]})
            else:
                url = "https://api.notion.com/v1/pages"
                res = requests.post(url, headers=headers, json=payload)
            
            if res.status_code == 200:
                st.success("🎯 Sucesso!"); navegar("🏠 HOME")
            else: st.error("Erro no Notion.")

# --- TELA GRADE (BOTÕES EDIÇÃO E PDF) ---
elif st.session_state.pagina == "📊 GRADE":
    if st.button("⬅️ VOLTAR"): navegar("🏠 HOME")
    st.subheader("📊 Agendamentos Ativos")
    
    dados = carregar_dados_notion()
    if dados:
        for d in dados:
            with st.expander(f"O.S: {d['Nº OS']} - {d['CLIENTE']}"):
                col_info, col_botoes = st.columns([3, 1])
                with col_info:
                    st.write(f"**Início:** {d['INÍCIO']} | **Status:** {d['STATUS']}")
                    st.write(f"**Empurrador:** {d['EMPURRADOR']} | **Balsa:** {d['BALSA']}")
                
                with col_botoes:
                    if st.button("✏️ Editar", key=f"ed_{d['ID_NOTION']}"):
                        st.session_state.dados_edicao = d
                        navegar("📋 CADASTRO")
                    
                    pdf_bytes = gerar_pdf_transdourada(d)
                    st.download_button("📄 PDF O.S", pdf_bytes, f"OS_{d['Nº OS']}.pdf", "application/pdf", key=f"pdf_{d['ID_NOTION']}")
    else:
        st.info("Nenhuma O.S encontrada no Notion.")

# --- TELA FINANCEIRO ---
elif st.session_state.pagina == "💰 FINANCEIRO":
    if st.button("⬅️ VOLTAR"): navegar("🏠 HOME")
    st.header("💰 Financeiro")
    st.table(pd.DataFrame(columns=["DATA", "PEDIDO", "VALOR", "STATUS"]))
