import streamlit as st
import pandas as pd
from fpdf import FPDF
import base64

# 1. Configurações Iniciais
st.set_page_config(page_title="ZION TECNOLOGIA", layout="wide")

# Inicialização de "Bancos de Dados" (Session State)
if 'lista_empurradores' not in st.session_state:
    st.session_state.lista_empurradores = []
if 'db_os' not in st.session_state:
    st.session_state.db_os = []
if 'tela' not in st.session_state:
    st.session_state.tela = "HOME"

# --- FUNÇÃO PARA GERAR PDF ---
def gerar_pdf(dados):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="ZION TECNOLOGIA - RELATÓRIO DE O.S", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", size=12)
    for chave, valor in dados.items():
        pdf.cell(200, 10, txt=f"{chave}: {valor}", ln=True)
    
    return pdf.output(dest='S').encode('latin-1')

# --- BARRA LATERAL ---
with st.sidebar:
    st.image("LOGO.PNG", use_container_width=True)
    if st.button("🏠 MENU PRINCIPAL"):
        st.session_state.tela = "MENU_ICONES"
        st.rerun()
    st.divider()
    st.caption("Versão 2.0 - Identica ao Vídeo")

# --- TELA 1: HOME (CAPA) ---
if st.session_state.tela == "HOME":
    st.markdown("<h1 style='text-align: center;'>ZION TECNOLOGIA</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("LOGO.PNG", use_container_width=True)
        if st.button("🔵 ENTRAR NO SISTEMA", use_container_width=True):
            st.session_state.tela = "MENU_ICONES"
            st.rerun()

# --- TELA 2: MENU DE ÍCONES (PAINEL GESTÃO) ---
elif st.session_state.tela == "MENU_ICONES":
    st.markdown("<h2 style='text-align: center;'>PAINEL DE GESTÃO</h2>", unsafe_allow_html=True)
    st.divider()
    
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("⏳ AGENDAMENTO / PROGRAMAÇÃO", use_container_width=True):
            st.session_state.tela = "AGENDAMENTO"
            st.rerun()
    with c2:
        if st.button("💰 FINANCEIRO / LANÇAMENTOS", use_container_width=True):
            st.session_state.tela = "FINANCEIRO"
            st.rerun()
    with c3:
        if st.button("📝 NOVO CADASTRO (O.S/NOMES)", use_container_width=True):
            st.session_state.tela = "CADASTRO"
            st.rerun()

# --- TELA 3: CADASTRO (FORMULÁRIO IGUAL AO VÍDEO) ---
elif st.session_state.tela == "CADASTRO":
    st.title("📝 Cadastro de Missão")
    
    with st.expander("➕ CADASTRAR NOME DO EMPURRADOR"):
        nome_novo = st.text_input("Nome do Colaborador:").upper()
        if st.button("SALVAR NOME"):
            st.session_state.lista_empurradores.append(nome_novo)
            st.success("Nome adicionado!")
            st.rerun()

    with st.form("form_registro"):
        col1, col2 = st.columns(2)
        with col1:
            pedido = st.text_input("PEDIDO")
            os_num = st.text_input("NÚMERO DA O.S")
            data = st.date_input("DATA")
        with col2:
            empurrador = st.selectbox("EMPURRADOR", options=st.session_state.lista_empurradores)
            local = st.text_input("LOCAL")
            valor_os = st.number_input("VALOR DA O.S (R$)", min_value=0.0)
        
        if st.form_submit_button("✅ SALVAR E VER AGENDAMENTO"):
            novo_registro = {
                "ID": len(st.session_state.db_os) + 1,
                "PEDIDO": pedido,
                "O.S": os_num,
                "DATA": str(data),
                "EMPURRADOR": empurrador,
                "LOCAL": local,
                "VALOR": valor_os,
                "STATUS": "ABERTA"
            }
            st.session_state.db_os.append(novo_registro)
            st.session_state.tela = "AGENDAMENTO"
            st.rerun()

# --- TELA 4: AGENDAMENTO (TABELA CRUZADA COM PDF) ---
elif st.session_state.tela == "AGENDAMENTO":
    st.title("⏳ Tabela de Agendamentos e O.S")
    
    if st.session_state.db_os:
        df = pd.DataFrame(st.session_state.db_os)
        
        # Criando a tabela linha a linha para colocar o botão de PDF
        for index, row in df.iterrows():
            col_dados, col_pdf = st.columns([8, 2])
            with col_dados:
                st.write(f"**O.S:** {row['O.S']} | **Pedido:** {row['PEDIDO']} | **Empurrador:** {row['EMPURRADOR']} | **Status:** {row['STATUS']}")
            with col_pdf:
                pdf_data = gerar_pdf(row.to_dict())
                st.download_button(label="📄 PDF", data=pdf_data, file_name=f"OS_{row['O.S']}.pdf", mime="application/pdf", key=f"pdf_{index}")
            st.divider()
    else:
        st.info("Nenhum lançamento registrado.")
    
    if st.button("🔄 ATUALIZAR SISTEMA"):
        st.rerun()

# --- TELA 5: FINANCEIRO ---
elif st.session_state.tela == "FINANCEIRO":
    st.title("💰 Financeiro Cruzado")
    if st.session_state.db_os:
        df_fin = pd.DataFrame(st.session_state.db_os)
        total = df_fin['VALOR'].sum()
        st.metric("Total de O.S em Aberto", f"R$ {total:,.2f}")
        st.dataframe(df_fin[["O.S", "EMPURRADOR", "VALOR", "STATUS"]])
    else:
        st.info("Sem lançamentos financeiros.")
