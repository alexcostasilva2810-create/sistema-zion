import streamlit as st
import requests
import pandas as pd
import os
import base64
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

# --- CSS PARA GRADE E BOTÕES ---
st.markdown("""
    <style>
    .grade-zion { width: 100%; border-collapse: collapse; background-color: white; color: black; font-size: 13px; }
    .grade-zion th { border: 2px solid #000000 !important; background-color: #f0f2f6; padding: 10px; text-align: left; }
    .grade-zion td { border: 2px solid #000000 !important; padding: 8px; }
    .stButton>button { width: 100%; border-radius: 8px; font-weight: bold; height: 3.5em; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNÇÃO GERAR PDF (MODELO TRANSDOURADA REPLICADO) ---
def gerar_pdf_os(d):
    pdf = FPDF()
    pdf.add_page()
    
    # Cabeçalho Logos (Simulado)
    pdf.set_font("Arial", "B", 10)
    pdf.cell(0, 5, "ZION TECNOLOGIA | TRANSDOURADA", ln=True)
    pdf.set_font("Arial", "", 8)
    pdf.cell(0, 5, "Navegação Ltda.    GRUPO DIAS", ln=True)
    pdf.ln(10)

    # Títulos Centralizados
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Solicitação de Escolta", ln=True, align="C")
    pdf.set_font("Arial", "B", 11)
    pdf.cell(0, 7, "ORDEM DE SERVIÇO", ln=True, align="C")
    pdf.cell(0, 7, f"O.S: {d['Nº OS']}", ln=True, align="C")
    pdf.set_font("Arial", "", 10)
    pdf.cell(0, 7, f"STATUS: {d['STATUS'].upper()}", ln=True, align="C")
    pdf.ln(2)

    # Caixa Solicitante (Conforme anexo)
    pdf.set_font("Arial", "B", 11)
    pdf.cell(0, 10, f"SOLICITANTE ( {d['CLIENTE'].upper()} )", border=1, ln=True, align="C")
    pdf.ln(5)

    # Grid de Informações
    pdf.set_font("Arial", "", 9)
    y = pdf.get_y()
    pdf.text(10, y, f"EMPURRADOR: {d.get('EMPURRADOR', '---')}")
    pdf.text(80, y, f"SAÍDA PREVISTA: {d.get('HORA_EMBARQUE', '---')}")
    pdf.text(150, y, f"STATUS: {d['STATUS']}")
    
    pdf.text(10, y+6, f"ORIGEM: {d.get('LOCAL', '---')}")
    pdf.text(80, y+6, f"DESTINO: {d.get('DESTINO', '---')}")
    pdf.text(150, y+6, f"SERVIÇO: {d['SERVIÇO']}")
    
    pdf.text(10, y+12, f"BALSA: {d.get('BALSA', '---')}")
    pdf.ln(20)

    # Faixa PVH-SEG
    pdf.set_font("Arial", "B", 11)
    pdf.cell(0, 10, "PVH-SEG Serv. de Vig. Patrimonial Ltda", border=1, ln=True, align="C")
    pdf.ln(5)

    # Datas
    pdf.set_font("Arial", "", 10)
    pdf.cell(0, 6, f"INÍCIO DA MISSÃO: {d['INÍCIO']}", ln=True)
    pdf.cell(0, 6, f"ESCOLTA 1: {d.get('ESCOLTA 1', '---')}", ln=True)
    pdf.cell(0, 6, f"ESCOLTA 2: {d.get('ESCOLTA 2', '---')}", ln=True)
    pdf.cell(0, 6, f"FIM DA MISSÃO: {d['DT SAÍDA']}", ln=True)
    
    pdf.ln(5)
    pdf.cell(190, 0, "", border="T", ln=True)
    pdf.ln(5)

    # Detalhamento (Onde entra a Descrição longa)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "DETALHAMENTO DA MISSÃO.", ln=True, align="C")
    pdf.set_font("Arial", "", 10)
    pdf.multi_cell(0, 6, f"DESCRIÇÃO: {d.get('DESCRIÇÃO', '---')}")

    # Rodapé
    pdf.set_y(-40)
    pdf.cell(190, 0, "", border="T", ln=True)
    pdf.cell(0, 10, "ASSINATURA RESPONSÁVEL", ln=True, align="C")
    pdf.set_font("Arial", "B", 7)
    pdf.cell(0, 5, "TRANSDOURADA NAVEGAÇÃO LTDA - ANANINDEUA/PA", ln=True, align="C")

    return pdf.output(dest="S").encode("latin-1")

# --- FUNÇÃO BUSCAR DADOS ---
def carregar_dados():
    try:
        url = f"https://api.notion.com/v1/databases/{DATABASE}/query"
        res = requests.post(url, headers=headers)
        if res.status_code == 200:
            results = res.json().get("results", [])
            lista = []
            for r in results:
                p = r["properties"]
                lista.append({
                    "ID": r["id"],
                    "Nº OS": p["Nº OS"]["title"][0]["plain_text"] if p["Nº OS"]["title"] else "---",
                    "CLIENTE": p["CLIENTE"]["rich_text"][0]["plain_text"] if p["CLIENTE"]["rich_text"] else "---",
                    "INÍCIO": p["INÍCIO DA MISSÃO"]["date"]["start"] if p["INÍCIO DA MISSÃO"]["date"] else "---",
                    "DT SAÍDA": p["DT SAÍDA"]["date"]["start"] if p["DT SAÍDA"]["date"] else "---",
                    "SERVIÇO": p["SERVIÇO"]["select"]["name"] if p["SERVIÇO"]["select"] else "---",
                    "STATUS": p["STATUS"]["select"]["name"] if p["STATUS"]["select"] else "---",
                    "EMPURRADOR": p["EMPURRADOR"]["rich_text"][0]["plain_text"] if p["EMPURRADOR"]["rich_text"] else "---",
                    "BALSA": p["BALSA"]["rich_text"][0]["plain_text"] if p["BALSA"]["rich_text"] else "---",
                    "LOCAL": p["LOCAL"]["rich_text"][0]["plain_text"] if p.get("LOCAL") and p["LOCAL"]["rich_text"] else "---",
                    "DESTINO": p["DESTINO"]["rich_text"][0]["plain_text"] if p.get("DESTINO") and p["DESTINO"]["rich_text"] else "---",
                    "HORA_EMBARQUE": p["HORA DE EMBARQUE"]["rich_text"][0]["plain_text"] if p.get("HORA DE EMBARQUE") and p["HORA DE EMBARQUE"]["rich_text"] else "---",
                    "DESCRIÇÃO": p["DESCRIÇÃO"]["rich_text"][0]["plain_text"] if p["DESCRIÇÃO"]["rich_text"] else "---",
                    "ESCOLTA 1": p["ESCOLTA 1"]["rich_text"][0]["plain_text"] if p["ESCOLTA 1"]["rich_text"] else "---",
                    "ESCOLTA 2": p["ESCOLTA 2"]["rich_text"][0]["plain_text"] if p["ESCOLTA 2"]["rich_text"] else "---"
                })
            return lista
    except: return []
    return []

# --- NAVEGAÇÃO ---
if "pagina" not in st.session_state: st.session_state.pagina = "🏠 HOME"

def navegar(p):
    st.session_state.pagina = p
    st.rerun()

# --- TELA HOME (ÍCONES RESTAURADOS) ---
if st.session_state.pagina == "🏠 HOME":
    if os.path.exists("LOGO.PNG"):
        st.image("LOGO.PNG", width=250)
    
    st.title("🛡️ Sistema Zion - Gestão Operacional")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📋 NOVO LANÇAMENTO"): navegar("📋 CADASTRO")
    with col2:
        if st.button("📊 VER AGENDAMENTOS"): navegar("📊 GRADE")
    with col3:
        if st.button("💰 FINANCEIRO"): navegar("💰 FINANCEIRO")

    st.markdown("---")
    st.subheader("📌 Status Rápido")
    st.info("Selecione uma das opções acima para operar o sistema.")

# --- TELA DA GRADE ---
elif st.session_state.pagina == "📊 GRADE":
    if st.button("⬅️ VOLTAR"): navegar("🏠 HOME")
    st.subheader("📋 Grade de Agendamentos Ativos")
    
    dados = carregar_dados()
    if dados:
        c = st.columns([1, 2, 1.2, 1.2, 1.2, 1.2, 0.8])
        header = ["O.S", "CLIENTE", "INÍCIO", "DT SAÍDA", "SERVIÇO", "STATUS", "PDF"]
        for i, h in enumerate(header): c[i].markdown(f"**{h}**")
        
        for item in dados:
            c = st.columns([1, 2, 1.2, 1.2, 1.2, 1.2, 0.8])
            c[0].write(item["Nº OS"])
            c[1].write(item["CLIENTE"])
            c[2].write(item["INÍCIO"])
            c[3].write(item["DT SAÍDA"])
            c[4].write(item["SERVIÇO"])
            c[5].write(item["STATUS"])
            with c[6]:
                pdf_data = gerar_pdf_os(item)
                st.download_button("📄", pdf_data, f"OS_{item['Nº OS']}.pdf", key=f"pdf_{item['ID']}")
    else:
        st.warning("Sem dados para exibir.")

# --- TELA CADASTRO (CALENDÁRIO DT SAÍDA OK) ---
elif st.session_state.pagina == "📋 CADASTRO":
    if st.button("⬅️ VOLTAR"): navegar("🏠 HOME")
    st.header("📝 Cadastro Geral de Missão")
    
    with st.form("form_final"):
        c1, c2, c3 = st.columns(3)
        os_n = c1.text_input("Nº O.S")
        ini_m = c1.date_input("INÍCIO DA MISSÃO", format="DD/MM/YYYY")
        dt_saida = c2.date_input("DT SAÍDA", format="DD/MM/YYYY") # CORREÇÃO: AGORA É CALENDÁRIO
        servico = c3.selectbox("SERVIÇO", ["Escolta", "Vigilância"])
        
        cliente = c1.text_input("CLIENTE")
        empurrador = c2.text_input("EMPURRADOR")
        balsa = c3.text_input("BALSA")
        
        local = c1.text_input("LOCAL")
        destino = c2.text_input("DESTINO")
        h_emb = c3.text_input("HORA DE EMBARQUE")

        esc1 = c1.text_input("ESCOLTA 1")
        esc2 = c2.text_input("ESCOLTA 2")
        status = c3.selectbox("STATUS", ["Em Andamento", "Encerrado"])
        
        desc = st.text_area("DESCRIÇÃO / OBSERVAÇÕES")
        
        if st.form_submit_button("✅ SALVAR OPERAÇÃO"):
            # REMOVIDO O CAMPO "VALOR" PARA EVITAR O ERRO 400
            payload = {
                "parent": {"database_id": DATABASE},
                "properties": {
                    "Nº OS": {"title": [{"text": {"content": os_n}}]},
                    "CLIENTE": {"rich_text": [{"text": {"content": cliente}}]},
                    "INÍCIO DA MISSÃO": {"date": {"start": str(ini_m)}},
                    "DT SAÍDA": {"date": {"start": str(dt_saida)}},
                    "SERVIÇO": {"select": {"name": servico}},
                    "STATUS": {"select": {"name": status}},
                    "EMPURRADOR": {"rich_text": [{"text": {"content": empurrador}}]},
                    "BALSA": {"rich_text": [{"text": {"content": balsa}}]},
                    "LOCAL": {"rich_text": [{"text": {"content": local}}]},
                    "DESTINO": {"rich_text": [{"text": {"content": destino}}]},
                    "HORA de EMBARQUE": {"rich_text": [{"text": {"content": h_emb}}]},
                    "ESCOLTA 1": {"rich_text": [{"text": {"content": esc1}}]},
                    "ESCOLTA 2": {"rich_text": [{"text": {"content": esc2}}]},
                    "DESCRIÇÃO": {"rich_text": [{"text": {"content": desc}}]}
                }
            }
            res = requests.post("https://api.notion.com/v1/pages", headers=headers, json=payload)
            if res.status_code == 200:
                st.success("🎯 Salvo com sucesso!")
                navegar("🏠 HOME")
            else:
                st.error(f"Erro no Notion: {res.text}")

elif st.session_state.pagina == "💰 FINANCEIRO":
    if st.button("⬅️ VOLTAR"): navegar("🏠 HOME")
    st.title("💰 Financeiro")
    st.info("Módulo em manutenção.")
