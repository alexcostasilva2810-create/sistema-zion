import streamlit as st
import pandas as pd
from fpdf import FPDF
import os
from streamlit_gsheets import GSheetsConnection

# 1. CONFIGURAÇÃO E ESTILO
st.set_page_config(page_title="ZION TECNOLOGIA", layout="wide")

# CSS para esconder o botão de menu e ajustar as cores
st.markdown("""
    <style>
    div.stButton > button:first-child { background-color: #1E3A8A; color: white; font-weight: bold; }
    .stImage > img { cursor: pointer; }
    </style>
    """, unsafe_allow_html=True)

# 2. CONEXÃO COM GOOGLE SHEETS (Modo Privado para Escrita)
URL_PLANILHA = "https://docs.google.com/spreadsheets/d/1Rzm55i-k9PSlc3TUownF4wBiGkQz6laU-Lruy-dEZQM/edit?usp=sharing"

# IMPORTANTE: Usando a conexão oficial que requer os Secrets configurados
conn = st.connection("gsheets", type=GSheetsConnection)

def carregar_dados():
    try:
        # Tenta ler a planilha usando os Secrets
        return conn.read(spreadsheet=URL_PLANILHA, ttl="0")
    except:
        return pd.DataFrame(columns=[
            "O.S", "PEDIDO", "CLIENTE", "TIPO", "INICIO", "FIM", "HORA", "SAIDA", 
            "EMPURRADOR", "CMT", "ESCOLTA1", "ESCOLTA2", "LOCAL", "DESTINO", 
            "BALSA", "STATUS", "DESCRIÇÃO", "ASSINATURA", "DIAS", "TOTAL"
        ])

# Estados de navegação
if 'tela' not in st.session_state: st.session_state.tela = "HOME"
if 'exibir_form' not in st.session_state: st.session_state.exibir_form = False

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

# --- LOGICA DE TELAS ---

if st.session_state.tela == "HOME":
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if os.path.exists("LOGO.PNG"):
            st.image("LOGO.PNG", use_container_width=True)
            if st.button("🚀 ENTRAR NO SISTEMA", use_container_width=True):
                st.session_state.tela = "AGENDAMENTO"
                st.rerun()

elif st.session_state.tela in ["AGENDAMENTO", "FINANCEIRO"]:
    with st.sidebar:
        if os.path.exists("LOGO.PNG"): st.image("LOGO.PNG", use_container_width=True)
        st.divider()
        if st.button("⏳ AGENDAMENTO"): st.session_state.tela = "AGENDAMENTO"; st.rerun()
        if st.button("💰 FINANCEIRO"): st.session_state.tela = "FINANCEIRO"; st.rerun()
        st.divider()
        if st.button("🏠 SAIR"): st.session_state.tela = "HOME"; st.rerun()

    if st.session_state.tela == "AGENDAMENTO":
        st.title("⏳ Agendamento")
        
        if st.button("🔴 NOVO CADASTRO"):
            st.session_state.exibir_form = not st.session_state.exibir_form
            st.rerun()

        if st.session_state.exibir_form:
            with st.form("cadastro_os"):
                c1, c2, c3, c4 = st.columns(4)
                os_n = c1.text_input("Nº O.S")
                ped = c2.text_input("PEDIDO")
                cli = c3.text_input("CLIENTE")
                tipo = c4.selectbox("TIPO", ["ESCOLTA", "VIGILANTE"])
                
                c5, c6 = st.columns(2)
                ini = c5.date_input("INÍCIO", format="DD/MM/YYYY")
                fim = c6.date_input("FIM", format="DD/MM/YYYY")
                
                desc = st.text_area("DESCRIÇÃO")
                ass = st.text_input("ASSINATURA")

                if st.form_submit_button("✅ SALVAR OPERAÇÃO"):
                    dias = (fim - ini).days if (fim - ini).days > 0 else 1
                    total = dias * (1870.0 if tipo == "ESCOLTA" else 970.0)
                    
                    nova_linha = {
                        "O.S": os_n, "PEDIDO": ped, "CLIENTE": cli, "TIPO": tipo,
                        "INICIO": ini.strftime('%d/%m/%Y'), "FIM": fim.strftime('%d/%m/%Y'),
                        "STATUS": "ANDAMENTO", "DESCRIÇÃO": desc, "ASSINATURA": ass,
                        "DIAS": dias, "TOTAL": total
                    }
                    
                    df_atual = carregar_dados()
                    df_novo = pd.concat([df_atual, pd.DataFrame([nova_linha])], ignore_index=True)
                    
                    # Salva na Planilha
                    conn.update(spreadsheet=URL_PLANILHA, data=df_novo)
                    st.success("Salvo com sucesso!")
                    st.session_state.exibir_form = False
                    st.rerun()

        # Lista de Registros (Sempre visível se não estiver editando)
        st.subheader("📋 Operações Existentes")
        df_base = carregar_dados()
        if not df_base.empty:
            st.dataframe(df_base, use_container_width=True, hide_index=True)
            for i, row in df_base.iterrows():
                with st.expander(f"Opções O.S {row['O.S']}"):
                    pdf = gerar_pdf_os(row.to_dict())
                    st.download_button(f"📥 PDF O.S {row['O.S']}", pdf, f"OS_{row['O.S']}.pdf", key=f"d_{i}")

    elif st.session_state.tela == "FINANCEIRO":
        st.title("💰 Financeiro")
        df_fin = carregar_dados()
        if not df_fin.empty:
            total = pd.to_numeric(df_fin['TOTAL'], errors='coerce').sum()
            st.metric("Faturamento Previsto", f"R$ {total:,.2f}")
            st.dataframe(df_fin[["O.S", "CLIENTE", "TOTAL"]], use_container_width=True)
