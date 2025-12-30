import streamlit as st
import pandas as pd
from fpdf import FPDF
from datetime import datetime

# 1. Configuração de Layout
st.set_page_config(page_title="ZION TECNOLOGIA", layout="wide")

# 2. Inicialização de Dados
if 'lista_empurradores' not in st.session_state:
    st.session_state.lista_empurradores = []
if 'db_os' not in st.session_state:
    st.session_state.db_os = []
if 'tela' not in st.session_state:
    st.session_state.tela = "HOME"

# --- FUNÇÃO PDF ---
def gerar_pdf(dados):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="ZION TECNOLOGIA - ORDEM DE SERVIÇO", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", size=10)
    for chave, valor in dados.items():
        pdf.cell(100, 8, txt=f"{chave}: {valor}", border=1)
        pdf.ln()
    return pdf.output(dest='S').encode('latin-1')

# --- NAVEGAÇÃO ---
with st.sidebar:
    st.image("LOGO.PNG", use_container_width=True)
    if st.button("🏠 MENU PRINCIPAL", use_container_width=True):
        st.session_state.tela = "MENU_ICONES"
        st.rerun()

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
    with st.expander("➕ CADASTRAR NOME DO EMPURRADOR"):
        nome_n = st.text_input("Nome:").upper()
        if st.button("ADICIONAR"):
            st.session_state.lista_empurradores.append(nome_n); st.rerun()

    with st.form("form_completo"):
        c1, c2 = st.columns(2)
        with c1:
            pedido = st.text_input("PEDIDO")
            os_n = st.text_input("NÚMERO DA O.S")
            # Data formatada para o padrão BR no seletor
            d_ini = st.date_input("INÍCIO DA MISSÃO", format="DD/MM/YYYY")
            h_emb = st.text_input("HORA DO EMBARQUE")
            local = st.text_input("LOCAL")
            tipo_servico = st.selectbox("TIPO DE SERVIÇO", ["ESCOLTA", "POSTO DE VIGILÂNCIA"])
        with c2:
            emp = st.selectbox("EMPURRADOR", options=st.session_state.lista_empurradores)
            cmt = st.text_input("CMT")
            saida = st.text_input("SAÍDA")
            d_fim = st.date_input("FIM DA MISSÃO", format="DD/MM/YYYY")
            h_term = st.text_input("HORA/TÉRMINO")
            status = st.selectbox("STATUS", ["ANDAMENTO", "ENCERRADO"])
        
        if st.form_submit_button("✅ SALVAR E REGISTRAR"):
            # Lógica Financeira
            dias = (d_fim - d_ini).days
            if dias <= 0: dias = 1
            
            valor_diaria = 1870.0 if tipo_servico == "ESCOLTA" else 970.0
            valor_total = dias * valor_diaria

            dados_os = {
                "PEDIDO": pedido, 
                "O.S": os_n, 
                "INÍCIO": d_ini.strftime('%d/%m/%Y'), # Salva formatado BR
                "FIM": d_fim.strftime('%d/%m/%Y'),    # Salva formatado BR
                "DIAS": dias, 
                "SERVIÇO": tipo_servico, 
                "EMPURRADOR": emp,
                "LOCAL": local, 
                "CMT": cmt, 
                "VALOR_TOTAL": valor_total, 
                "STATUS": status,
                "HORA_EMB": h_emb, 
                "HORA_TERM": h_term, 
                "SAÍDA": saida
            }
            st.session_state.db_os.append(dados_os)
            st.session_state.tela = "AGENDAMENTO"; st.rerun()

elif st.session_state.tela == "AGENDAMENTO":
    st.title("⏳ Agendamento de Missões (Operacional)")
    if st.session_state.db_os:
        df = pd.DataFrame(st.session_state.db_os)
        # Exibe dados operacionais sem valores financeiros
        cols_op = ["PEDIDO", "O.S", "INÍCIO", "FIM", "EMPURRADOR", "LOCAL", "CMT", "STATUS"]
        st.dataframe(df[cols_op], use_container_width=True)
        
        st.divider()
        for i, row in df.iterrows():
            with st.expander(f"Gerar PDF - O.S: {row['O.S']} ({row['EMPURRADOR']})"):
                pdf_bytes = gerar_pdf(row.to_dict())
                st.download_button(f"📥 BAIXAR PDF O.S {row['O.S']}", data=pdf_bytes, file_name=f"OS_{row['O.S']}.pdf", key=f"pdf_{i}")
    else:
        st.info("Nenhuma O.S registrada.")

elif st.session_state.tela == "FINANCEIRO":
    st.title("💰 Financeiro e Fechamento")
    if st.session_state.db_os:
        df_fin = pd.DataFrame(st.session_state.db_os)
        
        # Faturamento
        total_geral = df_fin['VALOR_TOTAL'].sum()
        st.metric("FATURAMENTO TOTAL ACUMULADO", f"R$ {total_geral:,.2f}")
        
        # Tabela Financeira com Datas em formato BR
        cols_fin = ["O.S", "PEDIDO", "INÍCIO", "FIM", "SERVIÇO", "DIAS", "VALOR_TOTAL"]
        st.table(df_fin[cols_fin])

        st.divider()
        st.subheader("📁 Anexar Notas Fiscais")
        for i, row in df_fin.iterrows():
            with st.expander(f"NF - O.S: {row['O.S']} (R$ {row['VALOR_TOTAL']:.2f})"):
                st.file_uploader(f"Anexar PDF da Nota Fiscal", key=f"nf_{i}")
    else:
        st.info("Aguardando lançamentos.")
