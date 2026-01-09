import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os

# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Zion Sistema", layout="wide")

def salvar_dados(lista):
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        # Nome EXATO do arquivo que está no seu GitHub
        arquivo_credenciais = "credenciais.json"
        
        if not os.path.exists(arquivo_credenciais):
            return False, f"O arquivo {arquivo_credenciais} não foi encontrado no servidor."

        creds = ServiceAccountCredentials.from_json_keyfile_name(arquivo_credenciais, scope)
        client = gspread.authorize(creds)
        
        # SEU ID FIXO DA PLANILHA
        ID_PLANILHA = "1Rzm55i-k9PSIc3TUownF4wBiGkQz6laU-Lruy-dEZQM"
        sheet = client.open_by_key(ID_PLANILHA).sheet1
        
        sheet.append_row(lista)
        return True, "Sucesso"
    except Exception as e:
        return False, str(e)

# INTERFACE
st.title("⚓ ZION SISTEMA - OPERACIONAL")

# Barra lateral para conferência
st.sidebar.subheader("Arquivos no Servidor")
st.sidebar.write(os.listdir("."))

with st.form("form_zion", clear_on_submit=True):
    os_val = st.text_input("Nº O.S")
    cliente_val = st.text_input("Cliente")
    servico_val = st.text_input("Serviço")
    
    if st.form_submit_button("💾 SALVAR NA BASE BD ZION"):
        # Organiza os dados para a planilha
        dados = [os_val, cliente_val, servico_val]
        
        sucesso, msg = salvar_dados(dados)
        if sucesso:
            st.success("✅ OS gravada com sucesso na planilha!")
            st.balloons()
        else:
            st.error(f"❌ Erro: {msg}")
