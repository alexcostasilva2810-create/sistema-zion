import streamlit as st
import pandas as pd
from fpdf import FPDF
import os
from datetime import datetime

# Configuração da Página
st.set_page_config(page_title="ZION TECNOLOGIA", layout="wide")

# Estilização Personalizada (Cores dos Botões)
st.markdown("""
    <style>
    div.stButton > button:first-child { background-color: #f44336; color: white; } /* Vermelho Geral */
    .st-emotion-cache-19rxjzoef { background-color: #4CAF50 !important; color: white !important; } /* Verde Salvar */
    </style>
    """, unsafe_allow_html=True)

# Inicialização do Banco de Dados
if 'db_os' not in st.session_state: st.session_state.db_os = []
if 'tela' not in st.session_state: st.session_state.tela = "HOME"
if 'exibir_form' not in st.session_state: st.session_state.exibir_form = False
if 'editando_idx' not in st.session_state: st.session_state.editando_idx = None

# --- FUNÇÃO GERADORA DE PDF O.S ---
def gerar_pdf_os(dados):
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.add_page()
    logo_pdf = "logo app.jpg"
    if os.path.exists(logo_pdf):
        try: pdf.image(logo_pdf, x=10, y=10, w=45)
        except: pass
    pdf.set_font("Arial", 'B', 14); pdf.ln(20)
    pdf.cell(0, 10, "ORDEM DE SERVIÇO DE ESCOLTA", ln=True, align='C')
    pdf.set_font("Arial", 'B', 10); pdf.cell(0, 7, f"CLIENTE: {str(dados.get('CLIENTE'))} | O.S: {str(dados.get('O.S'))}", ln=True, align='C')
    pdf.ln(5); pdf.line(10, pdf.get_y(), 200, pdf.get_y()); pdf.ln(5)
    campos = [("INÍCIO", "INICIO"), ("FIM", "FIM"), ("EMPURRADOR", "EMPURRADOR"), ("LOCAL", "LOCAL"), ("DESTINO", "DESTINO"), ("STATUS", "STATUS")]
    pdf.set_font("Arial", size=10)
    for label, chave in campos:
        pdf.set_fill_color(240, 240, 240)
        pdf.cell(50, 7, txt=f" {label}:", border=1, fill=True)
        pdf.cell(140, 7, txt=f" {str(dados.get(chave, '---'))}", border=1); pdf.ln()
    pdf.ln(5); pdf.set_font("Arial", 'B', 10); pdf.cell(0, 8, "DETALHAMENTO:", ln=True)
    pdf.set_font("Arial", size=10); pdf.multi_cell(0, 7, txt=str(dados.get('DESCRIÇÃO', '---')), border=1)
    return pdf.output(dest='S').encode('latin-1', 'ignore')

# --- SIDEBAR ---
with st.sidebar:
    if os.path.exists("LOGO.PNG"):
        if st.button("🏠 MENU PRINCIPAL", key="btn_home_side"):
            st.session_state.tela = "MENU_ICONES"
            st.rerun()
        st.image("LOGO.PNG", use_container_width=True)

# --- TELAS ---

if st.session_state.tela == "HOME":
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if os.path.exists("LOGO.PNG"): st.image("LOGO.PNG", use_container_width=True)
        if st.button("🔵 ACESSAR SISTEMA", use_container_width=True):
            st.session_state.tela = "MENU_ICONES"; st.rerun()

elif st.session_state.tela == "MENU_ICONES":
    st.markdown("<h2 style='text-align: center;'>PAINEL DE GESTÃO</h2>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    if c1.button("⏳ AGENDAMENTO", use_container_width=True): st.session_state.tela = "AGENDAMENTO"; st.rerun()
    if c2.button("💰 FINANCEIRO", use_container_width=True): st.session_state.tela = "FINANCEIRO"; st.rerun()

elif st.session_state.tela == "AGENDAMENTO":
    # DASHBOARD
    if st.session_state.db_os:
        df_dash = pd.DataFrame(st.session_state.db_os)
        abertas = len(df_dash[df_dash['STATUS'].str.contains("ANDAMENTO")])
        fechadas = len(df_dash[df_dash['STATUS'].str.contains("ENCERRADO")])
        m1, m2, m3 = st.columns(3)
        m1.metric("O.S. EM ANDAMENTO", abertas)
        m2.metric("O.S. ENCERRADAS", fechadas)
        m3.metric("TOTAL DE OPERAÇÕES", len(df_dash))
    
    st.divider()
    
    # Botão Vermelho para Novo Cadastro
    if st.button("➕ NOVO CADASTRO", type="secondary"):
        st.session_state.exibir_form = not st.session_state.exibir_form

    if st.session_state.exibir_form:
        with st.form("f_cadastro", clear_on_submit=True):
            st.subheader("📝 Dados da Nova Operação")
            c1, c2, c3 = st.columns(3)
            cli = c1.text_input("CLIENTE", value="TRANSDOURADA")
            tipo = c1.selectbox("TIPO", ["ESCOLTA", "VIGILANTE"])
            os_n = c1.text_input("Nº O.S")
            ini = c2.date_input("INÍCIO", format="DD/MM/YYYY")
            fim = c2.date_input("FIM", format="DD/MM/YYYY")
            emp = c3.text_input("EMPURRADOR")
            cmt = c3.text_input("CMT")
            stt = st.selectbox("STATUS", ["ANDAMENTO", "ENCERRADO"])
            r1, r2, r3 = st.columns(3)
            ori, dest, bal = r1.text_input("LOCAL"), r2.text_input("DESTINO"), r3.text_input("BALSA")
            desc = st.text_area("DESCRIÇÃO")
            
            if st.form_submit_button("✅ SALVAR OPERAÇÃO"):
                dias = (fim - ini).days if (fim - ini).days > 0 else 1
                v_diaria = 1870.0 if tipo == "ESCOLTA" else 970.0
                st.session_state.db_os.append({
                    "O.S": os_n, "INICIO": ini.strftime('%d/%m/%Y'), "FIM": fim.strftime('%d/%m/%Y'),
                    "DT_OBJ": ini, "DIAS": dias, "TIPO": tipo, "TOTAL": dias * v_diaria,
                    "LOCAL": ori, "EMPURRADOR": emp, "CMT": cmt, "CLIENTE": cli, 
                    "BALSA": bal, "DESTINO": dest, "STATUS": "⏳ ANDAMENTO" if stt == "ANDAMENTO" else "✅ ENCERRADO",
                    "DESCRIÇÃO": desc
                })
                st.session_state.exibir_form = False
                st.rerun()

    # TABELA DE AGENDAMENTOS
    if st.session_state.db_os:
        st.write("### 📋 Operações Registradas")
        df = pd.DataFrame(st.session_state.db_os)
        st.dataframe(df[["O.S", "INICIO", "FIM", "EMPURRADOR", "CLIENTE", "STATUS"]], use_container_width=True, hide_index=True)
        
        for i, row in df.iterrows():
            with st.expander(f"⚙️ AÇÕES: O.S {row['O.S']} - {row['EMPURRADOR']}"):
                col_ed, col_pr = st.columns(2)
                if col_ed.button(f"🟠 EDITAR O.S {row['O.S']}", key=f"ed_{i}"):
                    st.session_state.editando_idx = i; st.session_state.tela = "EDITAR"; st.rerun()
                pdf_bytes = gerar_pdf_os(row.to_dict())
                col_pr.download_button(f"📥 IMPRIMIR O.S {row['O.S']}", data=pdf_bytes, file_name=f"OS_{row['O.S']}.pdf", key=f"pdf_{i}")

elif st.session_state.tela == "FINANCEIRO":
    st.title("💰 Controle Financeiro")
    if st.session_state.db_os:
        df_f = pd.DataFrame(st.session_state.db_os)
        df_f['VALOR EXIBIDO'] = df_f.apply(lambda x: f"R$ {x['TOTAL']:,.2f}" if "ENCERRADO" in x['STATUS'] else "---", axis=1)
        st.table(df_f[["O.S", "CLIENTE", "STATUS", "VALOR EXIBIDO"]])
    if st.button("⬅️ VOLTAR"): st.session_state.tela = "MENU_ICONES"; st.rerun()

elif st.session_state.tela == "EDITAR":
    idx = st.session_state.editando_idx
    if idx is not None:
        st.title(f"🟠 Editar O.S {st.session_state.db_os[idx]['O.S']}")
        with st.form("f_ed"):
            novo_stt = st.selectbox("STATUS", ["ANDAMENTO", "ENCERRADO"])
            nova_desc = st.text_area("DESCRIÇÃO", value=st.session_state.db_os[idx]['DESCRIÇÃO'])
            if st.form_submit_button("💾 SALVAR ALTERAÇÕES"):
                st.session_state.db_os[idx]['STATUS'] = "⏳ ANDAMENTO" if novo_stt == "ANDAMENTO" else "✅ ENCERRADO"
                st.session_state.db_os[idx]['DESCRIÇÃO'] = nova_desc
                st.session_state.tela = "AGENDAMENTO"; st.rerun()
        if st.button("❌ CANCELAR"): st.session_state.tela = "AGENDAMENTO"; st.rerun()
