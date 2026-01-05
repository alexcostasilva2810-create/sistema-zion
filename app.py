import streamlit as st
import pandas as pd
from fpdf import FPDF
import os
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

# 1. CONFIGURAÇÃO INICIAL
st.set_page_config(page_title="ZION TECNOLOGIA", layout="wide")

# Link da sua planilha (Necessário estar como EDITOR no botão Compartilhar)
URL_PLANILHA = "https://docs.google.com/spreadsheets/d/1Rzm55i-k9PSlc3TUownF4wBiGkQz6laU-Lruy-dEZQM/edit?usp=sharing"

# 2. CONEXÃO COM GOOGLE SHEETS (Usando Secrets para permitir gravação)
try:
    conn = st.connection("gsheets", type=GSheetsConnection, secrets=st.secrets["connections"]["gsheets"])
except Exception:
    # Caso os secrets ainda não estejam configurados no painel do Streamlit
    conn = st.connection("gsheets", type=GSheetsConnection)

def carregar_dados():
    try:
        return conn.read(spreadsheet=URL_PLANILHA, ttl="0")
    except Exception:
        return pd.DataFrame(columns=[
            "O.S", "PEDIDO", "CLIENTE", "TIPO", "INICIO", "FIM", "HORA", "SAIDA", 
            "EMPURRADOR", "CMT", "ESCOLTA1", "ESCOLTA2", "LOCAL", "DESTINO", 
            "BALSA", "STATUS", "DESCRIÇÃO", "ASSINATURA", "DIAS", "TOTAL"
        ])

# Inicialização de estados
if 'tela' not in st.session_state: st.session_state.tela = "HOME"
if 'exibir_form' not in st.session_state: st.session_state.exibir_form = False

# 3. FUNÇÃO PDF
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

# --- NAVEGAÇÃO ---

# TELA HOME (LOGO CLICÁVEL)
if st.session_state.tela == "HOME":
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.write("###")
        if os.path.exists("LOGO.PNG"):
            # Botão invisível sobre a logo para navegação
            if st.button("SISTEMA ZION - CLIQUE PARA ENTRAR", use_container_width=True):
                st.session_state.tela = "AGENDAMENTO"
                st.rerun()
            st.image("LOGO.PNG", use_container_width=True)
        else:
            if st.button("ENTRAR NO SISTEMA", use_container_width=True):
                st.session_state.tela = "AGENDAMENTO"
                st.rerun()

# TELA DE AGENDAMENTO
elif st.session_state.tela == "AGENDAMENTO":
    with st.sidebar:
        if os.path.exists("LOGO.PNG"): st.image("LOGO.PNG", use_container_width=True)
        if st.button("🏠 VOLTAR AO INÍCIO", use_container_width=True):
            st.session_state.tela = "HOME"
            st.rerun()

    st.title("⏳ Agendamento Zion")
    
    if st.button("🔴 NOVO CADASTRO"):
        st.session_state.exibir_form = not st.session_state.exibir_form
        st.rerun()

    if st.session_state.exibir_form:
        with st.form("f_cadastro", clear_on_submit=True):
            st.subheader("📝 Detalhes da Operação")
            c1, c2, c3, c4 = st.columns(4)
            os_n = c1.text_input("Nº O.S")
            ped = c2.text_input("PEDIDO")
            cli = c3.text_input("CLIENTE", value="TRANSDOURADA")
            tipo = c4.selectbox("TIPO", ["ESCOLTA", "VIGILANTE"])
            
            c5, c6, c7, c8 = st.columns(4)
            ini = c5.date_input("INÍCIO", format="DD/MM/YYYY")
            fim = c6.date_input("FIM", format="DD/MM/YYYY")
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
                    "INICIO": ini.strftime('%d/%m/%Y'),
                    "FIM": fim.strftime('%d/%m/%Y'),
                    "HORA": h_emb, "SAIDA": sai, "EMPURRADOR": emp, "CMT": cmt,
                    "ESCOLTA1": esc1, "ESCOLTA2": esc2, "LOCAL": loc, "DESTINO": dst,
                    "BALSA": bal, "STATUS": stt, "DESCRIÇÃO": desc, "ASSINATURA": ass,
                    "DIAS": dias, "TOTAL": f"R$ {total_val:,.2f}"
                }
                
                df_atual = carregar_dados()
                df_novo = pd.concat([df_atual, pd.DataFrame([nova_os])], ignore_index=True)
                
                try:
                    conn.update(spreadsheet=URL_PLANILHA, data=df_novo)
                    st.success("Dados enviados com sucesso para a Planilha!")
                    st.session_state.exibir_form = False
                    st.rerun()
                except Exception as e:
                    st.error(f"Erro de permissão: Configure os Secrets no Streamlit. Detalhe: {e}")

    # EXIBIÇÃO
    df_visualizar = carregar_dados()
    if not df_visualizar.empty:
        st.dataframe(df_visualizar, use_container_width=True, hide_index=True)
        for idx, row in df_visualizar.iterrows():
            with st.expander(f"Opções O.S {row['O.S']}"):
                pdf_data = gerar_pdf_os(row.to_dict())
                st.download_button(
                    label=f"📥 Baixar PDF {row['O.S']}",
                    data=pdf_data,
                    file_name=f"OS_{row['O.S']}.pdf",
                    key=f"btn_{idx}"
                )
