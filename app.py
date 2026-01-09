import streamlit as st
import pandas as pd
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Zion Sistema", layout="wide")

# --- FUNÇÃO PARA CONECTAR AO GOOGLE SHEETS ---
def conectar_google_sheets():
    # Definição do escopo de acesso
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    
    # Carrega as credenciais do arquivo JSON que você baixou
    creds = ServiceAccountCredentials.from_json_keyfile_name('credenciais.json', scope)
    client = gspread.authorize(creds)
    
    # SEU ID DA PLANILHA (Extraído da sua imagem da URL)
    ID_PLANILHA = "1Rzm55i-k9PSIc3TUownF4wBiGkQz6laU-Lruy-dEZQM"
    
    # Abre a planilha pelo ID e seleciona a primeira aba
    sheet = client.open_by_key(ID_PLANILHA).sheet1
    return sheet

# --- INTERFACE DO SISTEMA ZION ---
st.title("⚓ ZION SISTEMA - CONTROLE OPERACIONAL")

# Criando as abas do sistema
aba1, aba2 = st.tabs(["📝 Lançamento", "📊 Extrato"])

with aba1:
    st.subheader("Nova Ordem de Serviço")
    
    with st.form("form_lancamento", clear_on_submit=True):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            f1_os = st.text_input("Nº O.S")
            f2_pedido = st.text_input("Nº Pedido")
            f3_cliente = st.text_input("Cliente")
            f4_tipo = st.selectbox("Tipo de Serviço", ["Escolta", "Empurrador", "Balsa", "Outros"])
            
        with col2:
            f5_inicio = st.date_input("Data Início")
            f6_fim = st.date_input("Data Fim")
            f7_hora = st.time_input("Horário")
            f8_saida = st.date_input("Data Saída")
            
        with col3:
            f9_empurrador = st.text_input("Empurrador")
            f10_escolta1 = st.text_input("Escolta 01")
            f11_escolta2 = st.text_input("Escolta 02")
            f12_local = st.text_input("Localização")

        col4, col5, col6 = st.columns(3)
        with col4:
            f13_destino = st.text_input("Destino")
            f14_balsa = st.text_input("Balsa")
        with col5:
            f15_status = st.selectbox("Status", ["Em andamento", "Concluído", "Pendente"])
            f16_desc = st.text_area("Descrição do Serviço")
        with col6:
            f17_assinatura = st.text_input("Assinado por")

        # BOTÃO DE SALVAR
        botao_salvar = st.form_submit_button("💾 SALVAR NA BASE BD ZION")

        if botao_salvar:
            try:
                # 1. Conecta na planilha
                sheet = conectar_google_sheets()
                
                # 2. Organiza os dados na ordem das colunas A até Q da sua planilha
                nova_linha = [
                    f1_os, f2_pedido, f3_cliente, f4_tipo, 
                    str(f5_inicio), str(f6_fim), str(f7_hora), str(f8_saida),
                    f9_empurrador, f10_escolta1, f11_escolta2, 
                    f12_local, f13_destino, f14_balsa, 
                    f15_status, f16_desc, f17_assinatura
                ]
                
                # 3. Envia para o Google Sheets
                sheet.append_row(nova_linha)
                
                st.success(f"✅ Sucesso! O.S {f1_os} registrada na planilha BD ZION.")
                st.balloons()
                
            except Exception as e:
                st.error(f"❌ Erro ao salvar: {e}")

with aba2:
    st.subheader("Consulta de Dados Real")
    if st.button("🔄 Atualizar Extrato"):
        try:
            sheet = conectar_google_sheets()
            dados = sheet.get_all_records()
            if dados:
                df = pd.DataFrame(dados)
                st.dataframe(df, use_container_width=True)
            else:
                st.warning("A planilha está vazia.")
        except Exception as e:
            st.error(f"Não foi possível carregar os dados: {e}")
