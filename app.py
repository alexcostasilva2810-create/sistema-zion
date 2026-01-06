import streamlit as st
import requests
from fpdf import FPDF
from datetime import datetime

# Configuração da Página Profissional
st.set_page_config(page_title="Zion Tecnologia - Gestão Integrada", layout="wide")

# Limpeza automática de segurança para o Token e ID
TOKEN = st.secrets["notion"]["token"].replace('"', '').replace('\\', '').strip()
DATABASE = st.secrets["notion"]["database_id"].replace('"', '').replace('\\', '').strip()

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

# --- FUNÇÕES DE SUPORTE ---
def buscar_todas_os():
    url = f"https://api.notion.com/v1/databases/{DATABASE}/query"
    try:
        res = requests.post(url, headers=headers)
        if res.status_code == 200:
            results = res.json().get("results", [])
            return [{"id": x["id"], 
                     "os": x["properties"]["Nº OS"]["title"][0]["text"]["content"] if x["properties"]["Nº OS"]["title"] else "000",
                     "cliente": x["properties"]["CLIENTE"]["rich_text"][0]["text"]["content"] if x["properties"]["CLIENTE"]["rich_text"] else "N/A",
                     "props": x["properties"]} for x in results]
    except: return []
    return []

def gerar_os_pdf(dados):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(190, 10, "Solicitação de Escolta", ln=True, align='C') # Estilo image_e40024.png
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(190, 7, "ORDEM DE SERVIÇO", ln=True, align='C')
    pdf.cell(190, 7, f"O.S: {dados.get('os')}", ln=True, align='C')
    pdf.ln(5)
    pdf.set_draw_color(0, 0, 0)
    pdf.cell(190, 10, f"SOLICITANTE ( {dados.get('cliente').upper()} )", border=1, ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(190, 10, "DETALHAMENTO DA MISSÃO.", ln=True, align='C')
    pdf.set_font("Arial", size=10)
    pdf.multi_cell(190, 6, dados.get('desc', '')) # Estilo image_e40024.png
    return pdf.output(dest='S').encode('latin-1')

# --- MENU DE NAVEGAÇÃO (CAPA NAVEGÁVEL) ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/9439/9439247.png", width=100) # Ícone Zion
st.sidebar.title("Zion Tecnologia")
menu = st.sidebar.radio("Navegação", ["📋 Cadastro de OS", "💰 Financeiro", "🖨️ Gestão e PDF"])

# --- TELA 1: CADASTRO E AGENDAMENTO ---
if menu == "📋 Cadastro de OS":
    st.title("🛡️ Cadastro de Operações")
    with st.form("form_cadastro", clear_on_submit=True):
        c1, c2 = st.columns(2)
        os_f = c1.text_input("Nº OS")
        cli_f = c1.text_input("CLIENTE")
        data_f = c2.date_input("INÍCIO DA MISSÃO")
        tipo_f = c2.selectbox("TIPO", ["ESCOLTA", "VIGILÂNCIA", "OUTROS"])
        desc_f = st.text_area("DETALHAMENTO DA MISSÃO")
        ass_f = st.text_input("ASSINATURA RESPONSÁVEL")
        
        if st.form_submit_button("✅ SALVAR OPERAÇÃO"):
            payload = {
                "parent": {"database_id": DATABASE},
                "properties": {
                    "Nº OS": {"title": [{"text": {"content": os_f}}]},
                    "CLIENTE": {"rich_text": [{"text": {"content": cli_cli_f}}]},
                    "TIPO": {"select": {"name": tipo_f}},
                    "DESCRIÇÃO": {"rich_text": [{"text": {"content": desc_f}}]},
                    "ASSINATURA": {"rich_text": [{"text": {"content": ass_f}}]}
                }
            }
            res = requests.post("https://api.notion.com/v1/pages", headers=headers, json=payload)
            if res.status_code == 200: st.success("🎯 Salvo com sucesso!")
            else: st.error(f"Erro: {res.text}")

# --- TELA 2: FINANCEIRO ---
elif menu == "💰 Financeiro":
    st.title("💰 Gestão Financeira Zion")
    st.info("Painel financeiro integrado à Ordem de Serviço.")
    with st.form("financeiro"):
        os_ref = st.text_input("Vincular ao Nº OS")
        vlr = st.number_input("Valor da Operação (R$)", min_value=0.0)
        status = st.selectbox("Status de Pagamento", ["Pendente", "Pago", "Faturado"])
        if st.form_submit_button("💰 Registrar Financeiro"):
            st.success(f"Financeiro da OS {os_ref} atualizado!")

# --- TELA 3: GESTÃO E PDF ---
elif menu == "🖨️ Gestão e PDF":
    st.title("🖨️ Emissão de Documentos")
    lista = buscar_todas_os()
    if lista:
        escolha = st.selectbox("Selecione a OS", [f"OS {x['os']} - {x['cliente']}" for x in lista])
        item = next(x for x in lista if f"OS {x['os']} - {x['cliente']}" == escolha)
        
        # Gerar os dados para o PDF igual à imagem
        dados_pdf = {
            "os": item['os'],
            "cliente": item['cliente'],
            "desc": item['props']['DESCRIÇÃO']['rich_text'][0]['text']['content'] if item['props']['DESCRIÇÃO']['rich_text'] else ""
        }
        
        pdf_bytes = gerar_os_pdf(dados_pdf)
        st.download_button(label="📄 BAIXAR PDF DA O.S", data=pdf_bytes, file_name=f"OS_{item['os']}.pdf")
    else:
        st.warning("Nenhuma OS encontrada.")
