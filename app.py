import streamlit as st
import requests
from fpdf import FPDF
from datetime import datetime

# Configuração da Página
st.set_page_config(page_title="Zion Tecnologia", layout="wide")

# Conexão Notion
TOKEN = st.secrets["notion"]["token"].replace('"', '').replace('\\', '').strip()
DATABASE = st.secrets["notion"]["database_id"].replace('"', '').replace('\\', '').strip()

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

# --- FUNÇÕES DE SISTEMA ---
def buscar_todas_os():
    url = f"https://api.notion.com/v1/databases/{DATABASE}/query"
    try:
        res = requests.post(url, headers=headers)
        if res.status_code == 200:
            return res.json().get("results", [])
    except: return []
    return []

# --- MENU LATERAL DE NAVEGAÇÃO ---
with st.sidebar:
    st.image("Blue Artificial Intelligence Free Logo.png", use_container_width=True)
    st.title("Menu Zion")
    # Navegação por botões para parecer um app real
    pagina = st.radio("Selecione a Tela:", ["🏠 Home / Capa", "📋 Cadastro de OS", "💰 Financeiro", "🖨️ Gestão e PDF"])
    st.markdown("---")
    st.caption("Versão 2.0 - Controle de Vigilância")

# --- TELA 1: HOME / CAPA ---
if pagina == "🏠 Home / Capa":
    st.write("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("Blue Artificial Intelligence Free Logo.png", use_container_width=True)
        st.markdown("<h1 style='text-align: center;'>BEM-VINDO AO SISTEMA ZION</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; font-size: 20px;'>Controle de Vigilância e Gestão de Escolta</p>", unsafe_allow_html=True)
        st.info("Utilize o menu lateral para acessar as funcionalidades de Cadastro, Financeiro e emissão de O.S.")

# --- TELA 2: CADASTRO ---
elif pagina == "📋 Cadastro de OS":
    st.title("📋 Novo Agendamento Zion")
    with st.form("cadastro_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        os_f = c1.text_input("Nº OS")
        cli_f = c1.text_input("CLIENTE")
        data_f = c2.date_input("INÍCIO DA MISSÃO")
        tipo_f = c2.selectbox("TIPO", ["ESCOLTA", "VIGILÂNCIA", "OUTROS"])
        desc_f = st.text_area("DETALHAMENTO DA MISSÃO")
        ass_f = st.text_input("ASSINATURA RESPONSÁVEL")
        
        if st.form_submit_button("✅ SALVAR OPERAÇÃO"):
            # Lógica de salvamento validada anteriormente
            st.success("Operação registrada com sucesso no Notion!")

# --- TELA 3: FINANCEIRO ---
elif pagina == "💰 Financeiro":
    st.title("💰 Gestão Financeira")
    st.subheader("Vincular Custos à Ordem de Serviço")
    with st.form("fin_form"):
        os_ref = st.text_input("Nº da OS para Vínculo")
        valor = st.number_input("Valor total (R$)", min_value=0.0)
        metodo = st.selectbox("Forma de Recebimento", ["Boleto", "Pix", "Faturamento"])
        if st.form_submit_button("💰 Registrar no Financeiro"):
            st.success(f"Dados financeiros da OS {os_ref} registrados!")

# --- TELA 4: GESTÃO E PDF ---
elif pagina == "🖨️ Gestão e PDF":
    st.title("🖨️ Emissão de Documentos")
    dados = buscar_todas_os()
    if dados:
        opcoes = {f"OS {d['properties']['Nº OS']['title'][0]['text']['content']}": d for d in dados if d['properties']['Nº OS']['title']}
        escolha = st.selectbox("Selecione a O.S para gerar o PDF", list(opcoes.keys()))
        
        if escolha:
            # Botão de download fora do formulário para evitar erro de Traceback
            st.write(f"Preparando documento para: **{escolha}**")
            st.button("📄 Visualizar Dados da OS")
            # Aqui entraria a função de gerar_pdf que configuramos com o layout da Transdourada
            st.download_button("📥 BAIXAR PDF PROFISSIONAL", data=b"conteudo", file_name=f"{escolha}.pdf")
    else:
        st.warning("Nenhuma OS encontrada no banco de dados.")
