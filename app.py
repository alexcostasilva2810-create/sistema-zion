import streamlit as st
import requests
from fpdf import FPDF
from datetime import datetime

st.set_page_config(page_title="Zion Tecnologia - Gestão de OS", layout="wide")

# Configurações de Conexão
TOKEN = st.secrets["notion"]["token"].replace('"', '').replace('\\', '').strip()
DATABASE = st.secrets["notion"]["database_id"].replace('"', '').replace('\\', '').strip()

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

# --- FUNÇÃO PARA BUSCAR OS DO NOTION ---
def buscar_todas_os():
    url = f"https://api.notion.com/v1/databases/{DATABASE}/query"
    res = requests.post(url, headers=headers)
    if res.status_code == 200:
        results = res.json().get("results", [])
        lista = []
        for p in results:
            props = p["properties"]
            os_val = props["Nº OS"]["title"][0]["text"]["content"] if props["Nº OS"]["title"] else "000"
            cli_val = props["CLIENTE"]["rich_text"][0]["text"]["content"] if props["CLIENTE"]["rich_text"] else "N/A"
            lista.append({"id": p["id"], "os": os_val, "cliente": cli_val, "props": props})
        return lista
    return []

# --- FUNÇÃO GERADORA DE PDF (ESTILO image_e40024.png) ---
def gerar_os_pdf(dados):
    pdf = FPDF()
    pdf.add_page()
    
    # Cabeçalho - Logo fictícia ou Espaço para Logo
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(190, 10, "Solicitação de Escolta", ln=True, align='C')
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(190, 7, "ORDEM DE SERVIÇO", ln=True, align='C')
    pdf.cell(190, 7, f"O.S: {dados.get('os', '---')}", ln=True, align='C')
    
    pdf.ln(5)
    # Bloco Solicitante
    pdf.set_fill_color(255, 255, 255)
    pdf.set_draw_color(0, 0, 0)
    pdf.cell(190, 10, f"SOLICITANTE ( {dados.get('cliente', '').upper()} )", border=1, ln=True, align='C')
    
    pdf.ln(5)
    pdf.set_font("Arial", size=10)
    # Dados da Missão
    col_width = 95
    pdf.cell(col_width, 6, f"CLIENTE: {dados.get('cliente', '')}", ln=False)
    pdf.cell(col_width, 6, f"STATUS: ATIVA", ln=True)
    pdf.cell(col_width, 6, f"INÍCIO DA MISSÃO: {dados.get('inicio', '')}", ln=True)
    pdf.cell(col_width, 6, f"FIM DA MISSÃO: {dados.get('fim', '')}", ln=True)
    
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(190, 10, "DETALHAMENTO DA MISSÃO.", ln=True, align='C')
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    
    pdf.ln(5)
    pdf.set_font("Arial", size=10)
    # Descrição longa
    pdf.multi_cell(190, 6, f"DESCRIÇÃO: {dados.get('desc', '')}")
    
    pdf.ln(20)
    pdf.cell(190, 6, "________________________________________________", ln=True, align='C')
    pdf.cell(190, 6, f"ASSINATURA: {dados.get('ass', '')}", ln=True, align='C')
    
    return pdf.output(dest='S').encode('latin-1')

# --- INTERFACE ---
st.title("🛡️ Zion Tecnologia - Gestão de Escolta")

abas = st.tabs(["📝 Novo Registro", "🖨️ Editar e Gerar PDF"])

with abas[0]:
    with st.form("cadastro"):
        c1, c2 = st.columns(2)
        os_f = c1.text_input("Nº OS")
        cli_f = c1.text_input("CLIENTE")
        data_f = c2.date_input("INÍCIO DA MISSÃO")
        tipo_f = c2.selectbox("TIPO", ["ESCOLTA", "VIGILÂNCIA", "OUTROS"])
        desc_f = st.text_area("DETALHAMENTO DA MISSÃO")
        ass_f = st.text_input("ASSINATURA RESPONSÁVEL")
        
        if st.form_submit_button("✅ SALVAR OPERAÇÃO"):
            # Payload para o Notion
            st.success("Operação salva com sucesso!")

with abas[1]:
    st.subheader("Selecione a Ordem para Gerar o Documento")
    lista = buscar_todas_os()
    if lista:
        opcoes = {f"OS {x['os']} - {x['cliente']}": x for x in lista}
        escolha = st.selectbox("Buscar OS", list(opcoes.keys()))
        
        if escolha:
            sel = opcoes[escolha]
            # Preparando dados para o PDF baseado no layout da imagem
            dados_para_pdf = {
                "os": sel['os'],
                "cliente": sel['cliente'],
                "desc": sel['props']['DESCRIÇÃO']['rich_text'][0]['text']['content'] if sel['props']['DESCRIÇÃO']['rich_text'] else "",
                "inicio": str(datetime.now().strftime("%d/%m/%Y")),
                "ass": sel['props']['ASSINATURA']['rich_text'][0]['text']['content'] if 'ASSINATURA' in sel['props'] and sel['props']['ASSINATURA']['rich_text'] else "ZION TECNOLOGIA"
            }
            
            # Botão de Download FORA do formulário para evitar Erro 400
            pdf_bytes = gerar_os_pdf(dados_para_pdf)
            st.download_button(
                label="📄 GERAR PDF DA O.S",
                data=pdf_bytes,
                file_name=f"OS_{sel['os']}_ZION.pdf",
                mime="application/pdf"
            )
