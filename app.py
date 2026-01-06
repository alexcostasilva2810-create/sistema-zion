import streamlit as st
import requests
import pandas as pd
import os
import base64
from fpdf import FPDF

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

# --- CSS PARA GRADE PROFISSIONAL ---
st.markdown("""
    <style>
    .grade-zion { width: 100%; border-collapse: collapse; background-color: white; color: black; font-size: 14px; }
    .grade-zion th { border: 2px solid #000000 !important; background-color: #f0f2f6; padding: 10px; text-align: left; }
    .grade-zion td { border: 2px solid #000000 !important; padding: 8px; }
    .stButton>button { width: 100%; border-radius: 5px; height: 2.5em; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNÇÃO GERAR PDF ---
def gerar_pdf(dados):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, "ZION TECNOLOGIA - ORDEM DE SERVIÇO", ln=True, align="C")
    pdf.ln(10)
    
    # Grid de informações no PDF
    pdf.set_font("Arial", "B", 12)
    pdf.cell(190, 10, f" O.S: {dados['Nº OS']}", border=1, ln=True, fill=False)
    pdf.set_font("Arial", "", 11)
    pdf.cell(95, 10, f" Cliente: {dados['CLIENTE']}", border=1)
    pdf.cell(95, 10, f" Status: {dados['STATUS']}", border=1, ln=True)
    pdf.cell(95, 10, f" Início: {dados['INÍCIO']}", border=1)
    pdf.cell(95, 10, f" Saída: {dados['DT SAÍDA']}", border=1, ln=True)
    pdf.cell(190, 10, f" Serviço: {dados['SERVIÇO']}", border=1, ln=True)
    
    pdf.ln(20)
    pdf.cell(190, 10, "________________________________________", ln=True, align="C")
    pdf.cell(190, 10, "Assinatura Responsável", ln=True, align="C")
    return pdf.output(dest="S").encode("latin-1")

# --- BUSCAR DADOS REAIS DO NOTION ---
def carregar_dados_notion():
    url = f"https://api.notion.com/v1/databases/{DATABASE}/query"
    res = requests.post(url, headers=headers)
    if res.status_code == 200:
        results = res.json().get("results", [])
        lista = []
        for row in results:
            p = row["properties"]
            lista.append({
                "ID": row["id"],
                "Nº OS": p["Nº OS"]["title"][0]["plain_text"] if p["Nº OS"]["title"] else "---",
                "CLIENTE": p["CLIENTE"]["rich_text"][0]["plain_text"] if p["CLIENTE"]["rich_text"] else "---",
                "INÍCIO": p["INÍCIO DA MISSÃO"]["date"]["start"] if p["INÍCIO DA MISSÃO"]["date"] else "---",
                "DT SAÍDA": p["DT SAÍDA"]["date"]["start"] if p["DT SAÍDA"]["date"] else "---",
                "SERVIÇO": p["SERVIÇO"]["select"]["name"] if p["SERVIÇO"]["select"] else "---",
                "STATUS": p["STATUS"]["select"]["name"] if p["STATUS"]["select"] else "---"
            })
        return lista
    return []

# --- NAVEGAÇÃO ---
if "pagina" not in st.session_state: st.session_state.pagina = "🏠 HOME"

# --- TELA HOME (GRADE COM PDF E EDIÇÃO) ---
if st.session_state.pagina == "🏠 HOME":
    st.image("LOGO.PNG", width=400) # Se não tiver o arquivo, ele apenas pula
    st.subheader("📋 Grade de Agendamentos e Operações")
    
    dados = carregar_dados_notion()
    
    if dados:
        # Criamos a tabela visualmente
        # No Streamlit, para botões dentro de tabelas, usamos colunas para simular a grade
        
        # Cabeçalho da Grade
        cols = st.columns([1, 2, 1.5, 1.5, 1.5, 1.5, 1, 1])
        headers_lista = ["O.S", "CLIENTE", "INÍCIO", "DT SAÍDA", "SERVIÇO", "STATUS", "PDF", "EDIT"]
        for i, h in enumerate(headers_lista):
            cols[i].markdown(f"**{h}**")
        
        st.divider()

        for item in dados:
            c1, c2, c3, c4, c5, c6, c7, c8 = st.columns([1, 2, 1.5, 1.5, 1.5, 1.5, 1, 1])
            c1.text(item["Nº OS"])
            c2.text(item["CLIENTE"])
            c3.text(item["INÍCIO"])
            c4.text(item["DT SAÍDA"])
            c5.text(item["SERVIÇO"])
            c6.text(item["STATUS"])
            
            # Botão de Impressão PDF
            with c7:
                pdf_bytes = gerar_pdf(item)
                st.download_button("📄", data=pdf_bytes, file_name=f"OS_{item['Nº OS']}.pdf", key=f"pdf_{item['ID']}")
            
            # Botão de Edição
            with c8:
                if st.button("✏️", key=f"edit_{item['ID']}"):
                    st.session_state.dados_edicao = item
                    st.session_state.pagina = "📋 AGENDAMENTO"
                    st.rerun()
    else:
        st.info("Nenhuma missão encontrada no Notion.")

    if st.button("➕ NOVO LANÇAMENTO"):
        st.session_state.pagina = "📋 AGENDAMENTO"
        st.rerun()

# --- TELA DE CADASTRO (Ajustada para Edição também) ---
elif st.session_state.pagina == "📋 AGENDAMENTO":
    st.header("📋 Lançamento / Edição de Missão")
    if st.button("⬅️ VOLTAR"): 
        st.session_state.pagina = "🏠 HOME"
        st.rerun()
    
    # (Aqui entra o seu formulário de 17 campos que já temos pronto)
    st.info("O formulário completo de 17 campos será carregado aqui para salvar no Notion.")
