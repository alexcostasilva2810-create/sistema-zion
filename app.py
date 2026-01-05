import streamlit as st
import pandas as pd
from fpdf import FPDF
import os
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

# CONFIGURAÇÃO
st.set_page_config(page_title="ZION TECNOLOGIA", layout="wide")

# LINK DA PLANILHA (Certifique-se de que está como EDITOR no compartilhar)
URL_PLANILHA = "https://docs.google.com/spreadsheets/d/1Rzm55i-k9PSlc3TUownF4wBiGkQz6laU-Lruy-dEZQM/edit?usp=sharing"

# CONEXÃO
conn = st.connection("gsheets", type=GSheetsConnection)

def carregar_dados():
    try:
        df = conn.read(spreadsheet=URL_PLANILHA, ttl="0")
        return df
    except:
        return pd.DataFrame(columns=["O.S", "PEDIDO", "CLIENTE", "TIPO", "INICIO", "FIM", "HORA", "SAIDA", "EMPURRADOR", "CMT", "ESCOLTA1", "ESCOLTA2", "LOCAL", "DESTINO", "BALSA", "STATUS", "DESCRIÇÃO", "ASSINATURA", "DIAS", "TOTAL"])

# ESTADOS
if 'db_os' not in st.session_state:
    st.session_state.db_os = carregar_dados()
if 'tela' not in st.session_state: st.session_state.tela = "AGENDAMENTO"
if 'exibir_form' not in st.session_state: st.session_state.exibir_form = False

# FUNÇÃO PDF
def gerar_pdf_os(dados):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "ORDEM DE SERVIÇO ZION", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", size=10)
    for k, v in dados.items():
        pdf.cell(50, 8, f"{k}:", border=1)
        pdf.cell(0, 8, f"{str(v)}", border=1, ln=True)
    return pdf.output(dest='S').encode('latin-1', 'ignore')

# TELA AGENDAMENTO
if st.session_state.tela == "AGENDAMENTO":
    st.title("⏳ Agendamento Zion")
    
    if st.button("🔴 NOVO CADASTRO"):
        st.session_state.exibir_form = not st.session_state.exibir_form
        st.rerun()

    if st.session_state.exibir_form:
        with st.form("f_cadastro", clear_on_submit=True):
            st.subheader("📝 Preencher Dados")
            c1, c2, c3, c4 = st.columns(4)
            os_n = c1.text_input("Nº O.S")
            ped = c2.text_input("PEDIDO")
            cli = c3.text_input("CLIENTE")
            tipo = c4.selectbox("TIPO", ["ESCOLTA", "VIGILANTE"])
            
            c5, c6 = st.columns(2)
            ini = c5.date_input("INÍCIO")
            fim = c6.date_input("FIM")
            
            desc = st.text_area("DESCRIÇÃO")
            ass = st.text_input("ASSINATURA")

            # Trecho corrigido para evitar os erros das imagens
if st.form_submit_button("✅ SALVAR OPERAÇÃO"):
    dias = (fim - ini).days if (fim - ini).days > 0 else 1
    total_val = dias * (1870.0 if tipo == "ESCOLTA" else 970.0)
    
    nova_os = {
        "O.S": os_n, "PEDIDO": ped, "CLIENTE": cli, "TIPO": tipo,
        "INICIO": ini.strftime('%d/%m/%Y'), "FIM": fim.strftime('%d/%m/%Y'),
        "STATUS": "ANDAMENTO", "DESCRIÇÃO": desc, "ASSINATURA": ass,
        "DIAS": dias, "TOTAL": total_val
    }
    
    # Salva na planilha e atualiza
    df_atual = carregar_dados()
    df_novo = pd.concat([df_atual, pd.DataFrame([nova_os])], ignore_index=True)
    conn.update(spreadsheet=URL_PLANILHA, data=df_novo)
    st.success("Salvo com sucesso!")
    st.rerun()

# Trecho do botão de download (corrigindo o SyntaxError da imagem)
pdf_bytes = gerar_pdf_os(row.to_dict())
st.download_button(
    label=f"📥 IMPRIMIR PDF {row['O.S']}",
    data=pdf_bytes,
    file_name=f"OS_{row['O.S']}.pdf",
    key=f"pdf_{i}"
)
    else:
        st.info("Planilha vazia ou aguardando dados.")
