import streamlit as st
import requests
import pandas as pd
import os
import base64
from fpdf import FPDF # Certifique-se de ter instalado: pip install fpdf

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Zion Tecnologia", layout="wide")

# --- CONEXÃO NOTION (Mantida) ---
TOKEN = st.secrets["notion"]["token"].replace('"', '').strip()
DATABASE = st.secrets["notion"]["database_id"].replace('"', '').strip()

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

# --- FUNÇÃO PARA CRIAR O PDF ---
def gerar_pdf_os(dados_os):
    pdf = FPDF()
    pdf.add_page()
    
    # Cabeçalho
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, "ZION TECNOLOGIA - ORDEM DE SERVIÇO", ln=True, align="C")
    pdf.ln(10)
    
    # Detalhes da O.S.
    pdf.set_font("Arial", "B", 12)
    pdf.set_fill_color(240, 242, 246)
    pdf.cell(190, 10, f" O.S Nº: {dados_os['os_n']}", border=1, ln=True, fill=True)
    
    pdf.set_font("Arial", "", 11)
    pdf.cell(95, 10, f" Cliente: {dados_os['cliente']}", border=1)
    pdf.cell(95, 10, f" Status: {dados_os['status']}", border=1, ln=True)
    
    pdf.cell(95, 10, f" Início Missão: {dados_os['ini_m']}", border=1)
    pdf.cell(95, 10, f" DT Saída: {dados_os['dt_saida']}", border=1, ln=True)
    
    pdf.cell(190, 10, f" Serviço: {dados_os['servico']}", border=1, ln=True)
    pdf.cell(190, 10, f" Local: {dados_os['local']}", border=1, ln=True)
    
    pdf.ln(5)
    pdf.set_font("Arial", "B", 11)
    pdf.cell(190, 10, " Equipe e Equipamento:", ln=True)
    pdf.set_font("Arial", "", 11)
    pdf.cell(63, 10, f" Escolta 1: {dados_os['esc1']}", border=1)
    pdf.cell(63, 10, f" Escolta 2: {dados_os['esc2']}", border=1)
    pdf.cell(64, 10, f" Balsa: {dados_os['balsa']}", border=1, ln=True)
    
    pdf.ln(10)
    pdf.set_font("Arial", "I", 10)
    pdf.multi_cell(190, 10, f"Descrição: {dados_os['desc']}", border=1)
    
    pdf.ln(20)
    pdf.cell(190, 10, "________________________________________", ln=True, align="C")
    pdf.cell(190, 10, "Assinatura do Responsável", ln=True, align="C")
    
    return pdf.output(dest="S").encode("latin-1")

# --- (O RESTANTE DO SEU CÓDIGO DE NAVEGAÇÃO E LOGO CONTINUA IGUAL) ---
# ... (Função navegar, logo_central, etc.)

# --- TELA DE RELATÓRIO (ONDE O PDF É GERADO) ---
if st.session_state.pagina == "📊 VER AGENDAMENTOS":
    if st.button("⬅️ VOLTAR"): st.session_state.pagina = "🏠 HOME"; st.rerun()
    st.header("📊 Gerenciamento de O.S")
    
    # Aqui simulamos a busca de um registro para gerar o PDF
    # Na prática, você selecionaria uma linha da tabela para imprimir
    st.write("Selecione uma O.S para gerar o documento PDF:")
    
    # Exemplo de botão para gerar o PDF do último cadastro (usando dados locais para teste)
    # No futuro, puxaremos os dados do Notion aqui.
    if st.button("📄 Gerar PDF da última O.S"):
        # Dados de exemplo (devem vir do seu formulário ou Notion)
        exemplo_dados = {
            "os_n": "12345", "cliente": "Exemplo Ltda", "status": "Em Andamento",
            "ini_m": "01/01/2026", "dt_saida": "02/01/2026", "servico": "Escolta",
            "local": "Porto", "esc1": "João", "esc2": "Maria", "balsa": "B-01",
            "desc": "Missão de escolta padrão."
        }
        
        pdf_bytes = gerar_pdf_os(exemplo_dados)
        st.download_button(
            label="📥 Baixar Ordem de Serviço em PDF",
            data=pdf_bytes,
            file_name=f"OS_{exemplo_dados['os_n']}.pdf",
            mime="application/pdf"
        )
