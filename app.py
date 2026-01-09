import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Zion Sistema", layout="wide")

# --- FUNÇÃO PARA SALVAR NO GOOGLE SHEETS ---
def salvar_dados_google(lista_dados):
    try:
        # Define os escopos necessários
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        
        # O arquivo deve estar na mesma pasta do GitHub
        arquivo_keys = "credenciais.json"
        
        if not os.path.exists(arquivo_keys):
            return False, f"Erro: Arquivo {arquivo_keys} não encontrado no servidor."

        # Autenticação
        creds = ServiceAccountCredentials.from_json_keyfile_name(arquivo_keys, scope)
        client = gspread.authorize(creds)
        
        # Abre a planilha pelo ID que confirmamos
        ID_PLANILHA = "1Rzm55i-k9PSIc3TUownF4wBiGkQz6laU-Lruy-dEZQM"
        sheet = client.open_by_key(ID_PLANILHA).sheet1
        
        # Adiciona a linha
        sheet.append_row(lista_dados)
        return True, "Sucesso"
    except Exception as e:
        return False, str(e)

# --- INTERFACE ---
st.title("⚓ ZION SISTEMA - CONTROLE OPERACIONAL")

with st.form("form_operacional", clear_on_submit=True):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        f1_os = st.text_input("Nº O.S")
        f2_pedido = st.text_input("Nº Pedido")
        f3_cliente = st.text_input("Cliente")
        f4_tipo = st.selectbox("Tipo", ["Escolta", "Empurrador", "Balsa"])

    with col2:
        f5_inicio = st.date_input("Início")
        f6_fim = st.date_input("Fim")
        f7_hora = st.time_input("Hora")
        f8_saida = st.date_input("Saída")

    with col3:
        f9_empurrador = st.text_input("Empurrador")
        f10_escolta1 = st.text_input("Escolta 01")
        f11_escolta2 = st.text_input("Escolta 02")
        f12_local = st.text_input("Local")

    f16_desc = st.text_area("Descrição do Serviço")
    
    if st.form_submit_button("💾 SALVAR NA BASE BD ZION"):
        # Organiza conforme as colunas A a Q da sua planilha
        linha = [
            f1_os, f2_pedido, f3_cliente, f4_tipo, 
            str(f5_inicio), str(f6_fim), str(f7_hora), str(f8_saida),
            f9_empurrador, f10_escolta1, f11_escolta2, f12_local,
            "", "", "", f16_desc, "" # Espaços vazios para colunas restantes
        ]
        
        sucesso, msg = salvar_dados_google(linha)
        if sucesso:
            st.success("✅ OS salva com sucesso na planilha!")
            st.balloons()
        else:
            st.error(f"❌ Falha: {msg}")
