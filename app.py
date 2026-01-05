import streamlit as st
import pandas as pd
from fpdf import FPDF
import os
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

# 1. CONFIGURAÇÃO INICIAL E ESTILO
st.set_page_config(page_title="ZION TECNOLOGIA", layout="wide")

st.markdown("""
    <style>
    div.stButton > button:first-child { background-color: #f44336; color: white; border-radius: 5px; height: 3em; font-weight: bold; }
    .st-emotion-cache-19rxjzoef { background-color: #4CAF50 !important; color: white !important; font-weight: bold !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. CONEXÃO COM GOOGLE SHEETS
# Link da sua planilha (Certifique-se de que a coluna A1 na planilha é "O.S")
URL_PLANILHA = "https://docs.google.com/spreadsheets/d/1Rzm55i-k9PSlc3TUownF4wBiGkQz6laU-Lruy-dEZQM/edit?usp=sharing"

conn = st.connection("gsheets", type=GSheetsConnection)

def carregar_dados():
    try:
        return conn.read(spreadsheet=URL_PLANILHA, ttl="0")
    except:
        return pd.DataFrame(columns=[
            "O.S", "PEDIDO", "CLIENTE", "TIPO", "INICIO", "FIM", "HORA", "SAIDA", 
            "EMPURRADOR", "CMT", "ESCOLTA1", "ESCOLTA2", "LOCAL", "DESTINO", 
            "BALSA", "STATUS", "DESCRIÇÃO", "ASSINATURA", "DIAS", "TOTAL"
        ])

# Inicialização da sessão
if 'db_os' not in st.session_state:
    st.session_state.db_os = carregar_dados()
if 'tela' not in st.session_state: 
    st.session_state.tela = "AGENDAMENTO"
if 'exibir_form' not in st.session_state: 
    st.session_state.exibir_form = False

# 3. FUNÇÃO PARA GERAR PDF
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

# 4. TELA DE AGENDAMENTO
if st.session_state.tela == "AGENDAMENTO":
    st.title("⏳ Agendamento Zion")
    
    col_nav = st.columns([1, 4])
    if col_nav[0].button("🔴 NOVO CADASTRO"):
        st.session_state.exibir_form = not st.session_state.exibir_form
        st.rerun()

    if st.session_state.exibir_form:
        with st.form("f_cadastro", clear_on_submit=True):
            st.subheader("📝 Preencher Dados")
            c1, c2, c3, c4 = st.columns(4)
            os_n = c1.text_input("Nº O.S")
            ped = c2.text_input("PEDIDO")
            cli = c3.text_input("CLIENTE", value="TRANSDOURADA")
            tipo = c4.selectbox("TIPO", ["ESCOLTA", "VIGILANTE"])
            
            c5, c6, c7, c8 = st.columns(4)
            ini = c5.date_input("INÍCIO")
            fim = c6.date_input("FIM")
            h_emb = c7.text_input("HORA EMBARQUE")
            sai = c8.text_input("SAÍDA")
            
            c9, c10, c11, c12 = st.columns(4)
            emp = c9.text_input("EMPURRADOR")
            cmt = c10.text_input("CMT")
            esc1 = c11.text_input("ESCOLTA 1")
            esc2 = c12.text_input("ESCOLTA 2")
            
            c13, c14, c15, c16 = st.columns(4)
            loc = c13.text_input("LOCAL ORIGEM")
            dst = c14.text_input("DESTINO")
            bal = c15.text_input("BALSA")
            stt = c16.selectbox("STATUS", ["ANDAMENTO", "ENCERRADO"])

            desc = st.text_area("DESCRIÇÃO")
            ass = st.text_input("ASSINATURA")

            if st.form_submit_button("✅ SALVAR OPERAÇÃO"):
                dias = (fim - ini).days if (fim - ini).days > 0 else 1
                valor_base = 1870.0 if tipo == "ESCOLTA" else 970.0
                total_val = dias * valor_base
                
                nova_os = {
                    "O.S": os_n, "PEDIDO": ped, "CLIENTE": cli, "TIPO": tipo,
                    "INICIO": ini.strftime('%d/%m/%Y'), "FIM": fim.strftime('%d/%m/%Y'),
                    "HORA": h_emb, "SAIDA": sai, "EMPURRADOR": emp, "CMT": cmt,
                    "ESCOLTA1": esc1, "ESCOLTA2": esc2, "LOCAL": loc, "DESTINO": dst,
                    "BALSA": bal, "STATUS": stt, "DESCRIÇÃO": desc, "ASSINATURA": ass,
                    "DIAS": dias, "TOTAL": total_val
                }
                
                # Salva na Planilha
                df_atual = carregar_dados()
                df_novo = pd.concat([df_atual, pd.DataFrame([nova_os])], ignore_index=True)
                conn.update(spreadsheet=URL_PLANILHA, data=df_novo)
                
                st.success("Dados salvos no Google Sheets!")
                st.session_state.exibir_form = False
                st.rerun()

    # 5. EXIBIÇÃO DA TABELA E PDF
    df_visualizar = carregar_dados()
    if not df_visualizar.empty:
        st.dataframe(df_visualizar, use_container_width=True, hide_index=True)
        
        for idx, row in df_visualizar.iterrows():
            with st.expander(f"Gerenciar O.S {row['O.S']}"):
                pdf_data = gerar_pdf_os(row.to_dict())
                st.download_button(
                    label=f"📥 Baixar PDF O.S {row['O.S']}",
                    data=pdf_data,
                    file_name=f"OS_{row['O.S']}.pdf",
                    key=f"btn_{idx}"
                )
    else:
        st.info("Aguardando o primeiro cadastro para exibir os dados.")
