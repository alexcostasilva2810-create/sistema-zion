import streamlit as st
import pandas as pd
from fpdf import FPDF
import os

# Configuração da Página
st.set_page_config(page_title="ZION TECNOLOGIA", layout="wide")

# Inicialização do Banco de Dados
if 'lista_empurradores' not in st.session_state:
    st.session_state.lista_empurradores = []
if 'db_os' not in st.session_state:
    st.session_state.db_os = []
if 'tela' not in st.session_state:
    st.session_state.tela = "HOME"

# --- FUNÇÃO GERADORA DE PDF A4 ---
def gerar_pdf_a4(dados):
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.add_page()
    
    # Tenta colocar a Logo
    try:
        if os.path.exists("LOGO.PNG"):
            pdf.image("LOGO.PNG", x=10, y=8, w=35)
    except:
        pass

    pdf.set_font("Arial", 'B', 18)
    pdf.cell(0, 15, "ZION TECNOLOGIA", ln=True, align='C')
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "ORDEM DE SERVIÇO", ln=True, align='C')
    pdf.ln(10)
    pdf.line(10, 45, 200, 45) # Linha horizontal
    pdf.ln(5)

    # Dados da O.S
    pdf.set_font("Arial", size=11)
    for chave, valor in dados.items():
        pdf.set_fill_color(240, 240, 240)
        pdf.cell(50, 10, txt=f"{chave}:", border=1, fill=True)
        pdf.cell(140, 10, txt=f"{str(valor)}", border=1)
        pdf.ln()

    # Espaço para Assinaturas
    pdf.ln(30)
    pdf.cell(95, 10, "__________________________", 0, 0, 'C')
    pdf.cell(95, 10, "__________________________", 0, 1, 'C')
    pdf.cell(95, 5, "RESPONSÁVEL ZION", 0, 0, 'C')
    pdf.cell(95, 5, "COLABORADOR", 0, 1, 'C')

    return pdf.output(dest='S').encode('latin-1')

# --- NAVEGAÇÃO ---
with st.sidebar:
    if os.path.exists("LOGO.PNG"):
        st.image("LOGO.PNG", use_container_width=True)
    if st.button("🏠 MENU PRINCIPAL", use_container_width=True):
        st.session_state.tela = "MENU_ICONES"
        st.rerun()

# --- TELAS ---
if st.session_state.tela == "HOME":
    st.markdown("<h1 style='text-align: center;'>ZION TECNOLOGIA</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if os.path.exists("LOGO.PNG"):
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
    st.title("📝 Cadastro de O.S")
    with st.expander("➕ CADASTRAR NOMES"):
        n = st.text_input("Nome:").upper()
        if st.button("SALVAR NOME"):
            st.session_state.lista_empurradores.append(n); st.rerun()

    with st.form("f_os"):
        c1, c2 = st.columns(2)
        with c1:
            ped = st.text_input("PEDIDO")
            os_n = st.text_input("NÚMERO DA O.S")
            d1 = st.date_input("INÍCIO DA MISSÃO", format="DD/MM/YYYY")
            tipo = st.selectbox("SERVIÇO", ["ESCOLTA", "POSTO DE VIGILÂNCIA"])
        with c2:
            emp = st.selectbox("EMPURRADOR", options=st.session_state.lista_empurradores)
            loc = st.text_input("LOCAL")
            d2 = st.date_input("FIM DA MISSÃO", format="DD/MM/YYYY")
            status = st.selectbox("STATUS", ["ANDAMENTO", "ENCERRADO"])
        
        if st.form_submit_button("✅ SALVAR"):
            dias = (d2 - d1).days if (d2 - d1).days > 0 else 1
            v_dia = 1870.0 if tipo == "ESCOLTA" else 970.0
            total = dias * v_dia
            
            st.session_state.db_os.append({
                "O.S": os_n, "PEDIDO": ped, "INÍCIO": d1.strftime('%d/%m/%Y'),
                "FIM": d2.strftime('%d/%m/%Y'), "EMPURRADOR": emp, "SERVIÇO": tipo,
                "DIAS": dias, "VALOR_TOTAL": total, "LOCAL": loc, "STATUS": status
            })
            st.session_state.tela = "AGENDAMENTO"; st.rerun()

elif st.session_state.tela == "AGENDAMENTO":
    st.title("⏳ Agendamento")
    if st.session_state.db_os:
        df = pd.DataFrame(st.session_state.db_os)
        st.dataframe(df[["O.S", "PEDIDO", "INÍCIO", "EMPURRADOR", "LOCAL", "STATUS"]], use_container_width=True)
        for i, row in df.iterrows():
            with st.expander(f"Imprimir O.S {row['O.S']}"):
                pdf_bytes = gerar_pdf_a4(row.to_dict())
                st.download_button(f"📥 BAIXAR PDF A4", data=pdf_bytes, file_name=f"OS_{row['O.S']}.pdf", key=f"pdf_{i}")
    else: st.info("Sem registros.")

elif st.session_state.tela == "FINANCEIRO":
    st.title("💰 Financeiro")
    if st.session_state.db_os:
        df_f = pd.DataFrame(st.session_state.db_os)
        st.metric("TOTAL FATURADO", f"R$ {df_f['VALOR_TOTAL'].sum():,.2f}")
        st.table(df_f[["O.S", "SERVIÇO", "DIAS", "VALOR_TOTAL"]])
        st.file_uploader("Anexar Nota Fiscal (PDF)", key="upload_nf")
    else: st.info("Sem dados.")
