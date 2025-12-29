import streamlit as st
import pandas as pd

# Configuração da Página
st.set_page_config(page_title="ZION TECNOLOGIA", layout="wide")

# Menu Lateral Estilizado
st.sidebar.markdown(f"""
    <div style="text-align: center;">
        <h2 style="color: #007bff;">ZION TECNOLOGIA</h2>
        <p>Controle de Vigilância</p>
    </div>
    """, unsafe_allow_html=True)

menu = st.sidebar.radio("Navegação", ["Início", "O.S PVH", "Financeiro", "Relatórios"])

if menu == "Início":
    st.title("Bem-vindo ao App de Gestão")
    st.info("Selecione uma opção no menu lateral para visualizar os dados.")

elif menu == "O.S PVH":
    st.subheader("📋 Ordens de Serviço")
    # Exemplo de dados baseados no seu vídeo
    dados_os = {
        'DATA': ['29/12/2025', '28/12/2025'],
        'MOTORISTA': ['SAMUEL PONTES', 'RODRIGO SANTANA'],
        'LOCAL': ['SANTARÉM', 'MANAUS'],
        'STATUS': ['FINALIZADO', 'EM ANDAMENTO']
    }
    st.table(pd.DataFrame(dados_os))

elif menu == "Financeiro":
    st.subheader("💰 Controle Financeiro")
    st.metric("Faturamento Mensal", "R$ 15.400,00", "+5%")
  
