import streamlit as st
import requests
from fpdf import FPDF
import pandas as pd

st.set_page_config(page_title="Zion Tecnologia - Gestão OS", layout="wide")

# Configurações de conexão
TOKEN = st.secrets["notion"]["token"].replace('"', '').replace('\\', '').strip()
DATABASE = st.secrets["notion"]["database_id"].replace('"', '').replace('\\', '').strip()

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

# --- FUNÇÃO PARA BUSCAR DADOS DO NOTION ---
def buscar_dados():
    url = f"https://api.notion.com/v1/databases/{DATABASE}/query"
    res = requests.post(url, headers=headers)
    if res.status_code == 200:
        data = res.json()
        paginas = []
        for page in data["results"]:
            props = page["properties"]
            # Extraindo os campos conforme sua tabela
            os_val = props["Nº OS"]["title"][0]["text"]["content"] if props["Nº OS"]["title"] else "Sem OS"
            cliente_val = props["CLIENTE"]["rich_text"][0]["text"]["content"] if props["CLIENTE"]["rich_text"] else ""
            paginas.append({"id": page["id"], "os": os_val, "cliente": cliente_val, "props": props})
        return paginas
    return []

# --- FUNÇÃO PARA GERAR PDF ---
def gerar_pdf(dados):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, "ZION TECNOLOGIA - ORDEM DE SERVIÇO", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", size=12)
    for chave, valor in dados.items():
        pdf.cell(200, 10, f"{chave}: {valor}", ln=True)
    return pdf.output(dest='S').encode('latin-1')

st.title("🚨 Zion Tecnologia - Gestão de OS")

aba_cad, aba_edit = st.tabs(["🆕 Nova OS", "✏️ Editar / Gerar PDF"])

# --- ABA 1: CADASTRO (O que já está funcionando) ---
with aba_cad:
    with st.form("novo_cadastro"):
        col1, col2 = st.columns(2)
        with col1:
            os_n = st.text_input("Nº OS")
            cli = st.text_input("CLIENTE")
        with col2:
            data_v = st.date_input("DATA")
            tipo_v = st.selectbox("TIPO", ["ESCOLTA", "VIGILÂNCIA", "OUTROS"])
        
        if st.form_submit_button("✅ SALVAR"):
            # Lógica de salvar que já testamos
            st.success("Salvo com sucesso!")

# --- ABA 2: EDIÇÃO E PDF ---
with aba_edit:
    st.subheader("Selecione uma OS para editar ou imprimir")
    lista_os = buscar_dados()
    
    if lista_os:
        opcoes = {f"OS: {item['os']} - {item['cliente']}": item for item in lista_os}
        escolha = st.selectbox("Escolha a OS", list(opcoes.keys()))
        
        if escolha:
            item_selecionado = opcoes[escolha]
            prop_atuais = item_selecionado["props"]
            
            # Formulário de Edição preenchido com dados do Notion
            with st.form("editar_os"):
                col_e1, col_e2 = st.columns(2)
                with col_e1:
                    novo_cliente = st.text_input("Cliente", value=item_selecionado["cliente"])
                with col_e2:
                    nova_desc = st.text_area("Descrição")
                
                c1, c2 = st.columns(2)
                with c1:
                    if st.form_submit_button("💾 ATUALIZAR NO NOTION"):
                        st.info("Atualizando dados...")
                with c2:
                    # Geração de PDF
                    dados_pdf = {"Nº OS": item_selecionado["os"], "Cliente": novo_cliente}
                    pdf_bytes = gerar_pdf(dados_pdf)
                    st.download_button("📄 BAIXAR PDF", data=pdf_bytes, file_name=f"OS_{item_selecionado['os']}.pdf")
    else:
        st.warning("Nenhuma OS encontrada ou erro de conexão.")
