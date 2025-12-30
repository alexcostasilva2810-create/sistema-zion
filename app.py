import streamlit as st
import pandas as pd
from fpdf import FPDF

# Configurações de Layout
st.set_page_config(page_title="ZION TECNOLOGIA", layout="wide")

# Inicialização de Banco de Dados
if 'lista_empurradores' not in st.session_state:
    st.session_state.lista_empurradores = []
if 'db_os' not in st.session_state:
    st.session_state.db_os = []
if 'tela' not in st.session_state:
    st.session_state.tela = "HOME"

# --- FUNÇÃO GERADORA DE PDF (COM TODOS OS CAMPOS) ---
def gerar_pdf(dados):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="ZION TECNOLOGIA - ORDEM DE SERVIÇO", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", size=10)
    
    # Criando as linhas do PDF
    for chave, valor in dados.items():
        pdf.cell(100, 8, txt=f"{chave}: {valor}", border=1)
        pdf.ln()
    return pdf.output(dest='S').encode('latin-1')

# --- NAVEGAÇÃO LATERAL ---
with st.sidebar:
    st.image("LOGO.PNG", use_container_width=True)
    if st.button("🏠 MENU PRINCIPAL", use_container_width=True):
        st.session_state.tela = "MENU_ICONES"
        st.rerun()
    st.divider()

# --- TELAS ---
if st.session_state.tela == "HOME":
    st.markdown("<h1 style='text-align: center;'>ZION TECNOLOGIA</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("LOGO.PNG", use_container_width=True)
        if st.button("🔵 ENTRAR NO SISTEMA", use_container_width=True):
            st.session_state.tela = "MENU_ICONES"
            st.rerun()

elif st.session_state.tela == "MENU_ICONES":
    st.markdown("<h2 style='text-align: center;'>PAINEL DE GESTÃO</h2>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("⏳ AGENDAMENTO", use_container_width=True):
            st.session_state.tela = "AGENDAMENTO"; st.rerun()
    with c2:
        if st.button("💰 FINANCEIRO", use_container_width=True):
            st.session_state.tela = "FINANCEIRO"; st.rerun()
    with c3:
        if st.button("📝 NOVO CADASTRO", use_container_width=True):
            st.session_state.tela = "CADASTRO"; st.rerun()

elif st.session_state.tela == "CADASTRO":
    st.title("📝 Cadastro de Missão")
    
    # Cadastro de nomes para a lista suspensa
    with st.expander("➕ CADASTRAR NOME DO EMPURRADOR"):
        nome_n = st.text_input("Nome:").upper()
        if st.button("ADICIONAR"):
            st.session_state.lista_empurradores.append(nome_n); st.rerun()

    with st.form("form_completo"):
        c1, c2 = st.columns(2)
        with c1:
            pedido = st.text_input("PEDIDO")
            os_n = st.text_input("NÚMERO DA O.S")
            d_ini = st.date_input("INÍCIO DA MISSÃO")
            h_emb = st.text_input("HORA DO EMBARQUE")
            local = st.text_input("LOCAL")
            esc1 = st.text_input("ESCOLTA 1")
            v_os = st.number_input("VALOR O.S", min_value=0.0)
        with c2:
            emp = st.selectbox("EMPURRADOR", options=st.session_state.lista_empurradores)
            cmt = st.text_input("CMT")
            saida = st.text_input("SAÍDA")
            d_fim = st.date_input("FIM DA MISSÃO")
            h_term = st.text_input("HORA/TÉRMINO")
            esc2 = st.text_input("ESCOLTA 2")
            status = st.selectbox("STATUS", ["ANDAMENTO", "ENCERRADO"])
        
        if st.form_submit_button("✅ SALVAR E REGISTRAR"):
            dados_os = {
                "PEDIDO": pedido, "O.S": os_n, "INÍCIO": str(d_ini), "EMBARQUE": h_emb,
                "LOCAL": local, "EMPURRADOR": emp, "CMT": cmt, "SAÍDA": saida,
                "FIM": str(d_fim), "TÉRMINO": h_term, "ESCOLTA 1": esc1, "ESCOLTA 2": esc2,
                "VALOR": v_os, "STATUS": status
            }
            st.session_state.db_os.append(dados_os)
            st.session_state.tela = "AGENDAMENTO"; st.rerun()

elif st.session_state.tela == "AGENDAMENTO":
    st.title("⏳ Agendamento e Programação Completa")
    
    if st.session_state.db_os:
        df = pd.DataFrame(st.session_state.db_os)
        
        # 1. Tabela Visual Completa (Exatamente como no vídeo)
        st.dataframe(df, use_container_width=True)
        
        st.divider()
        st.subheader("📄 Gerar Documentos Individuais")
        
        # 2. Área de Download (Linha por Linha)
        for i, row in df.iterrows():
            with st.expander(f"O.S: {row['O.S']} - {row['EMPURRADOR']}"):
                col_txt, col_btn = st.columns([7, 3])
                col_txt.write(f"Local: {row['LOCAL']} | CMT: {row['CMT']} | Valor: R$ {row['VALOR']}")
                pdf_bytes = gerar_pdf(row.to_dict())
                col_btn.download_button(f"📥 BAIXAR PDF O.S {row['O.S']}", data=pdf_bytes, file_name=f"OS_{row['O.S']}.pdf", key=f"pdf_{i}")
    else:
        st.info("Nenhuma O.S registrada.")

elif st.session_state.tela == "FINANCEIRO":
    st.title("💰 Financeiro Cruzado")
    if st.session_state.db_os:
        df_f = pd.DataFrame(st.session_state.db_os)
        st.metric("SALDO TOTAL O.S", f"R$ {df_f['VALOR'].sum():,.2f}")
        st.table(df_f[["O.S", "EMPURRADOR", "VALOR", "STATUS"]])
