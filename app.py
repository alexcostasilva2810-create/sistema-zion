import streamlit as st
import pandas as pd
from fpdf import FPDF
import os
from datetime import datetime

# Configuração da Página
st.set_page_config(page_title="ZION TECNOLOGIA", layout="wide")

# Estilização de Cores
st.markdown("""
    <style>
    div.stButton > button:first-child { background-color: #f44336; color: white; } /* Vermelho */
    .st-emotion-cache-19rxjzoef { background-color: #4CAF50 !important; color: white !important; } /* Verde Salvar */
    </style>
    """, unsafe_allow_html=True)

# Inicialização do Banco de Dados
if 'db_os' not in st.session_state: st.session_state.db_os = []
if 'tela' not in st.session_state: st.session_state.tela = "HOME"
if 'exibir_form' not in st.session_state: st.session_state.exibir_form = False

# --- FUNÇÃO GERADORA DE PDF ---
def gerar_pdf_os(dados):
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.add_page()
    if os.path.exists("logo app.jpg"):
        try: pdf.image("logo app.jpg", x=80, y=10, w=45); pdf.ln(30)
        except: pdf.ln(10)
    
    pdf.set_font("Arial", 'B', 14); pdf.cell(0, 10, "ORDEM DE SERVIÇO DE ESCOLTA", ln=True, align='C')
    pdf.set_font("Arial", 'B', 10); pdf.cell(0, 7, f"CLIENTE: {dados.get('CLIENTE')} | O.S: {dados.get('O.S')} | TIPO: {dados.get('TIPO')}", ln=True, align='C')
    pdf.ln(5); pdf.line(10, pdf.get_y(), 200, pdf.get_y()); pdf.ln(5)

    campos = [
        ("INÍCIO", "INICIO"), ("FIM", "FIM"), ("SAÍDA", "SAIDA"), ("HORA EMBARQUE", "HORA"),
        ("TIPO SERVIÇO", "TIPO"), ("EMPURRADOR", "EMPURRADOR"), ("CMT", "CMT"),
        ("ESCOLTA 1", "ESCOLTA1"), ("ESCOLTA 2", "ESCOLTA2"), ("LOCAL", "LOCAL"),
        ("DESTINO", "DESTINO"), ("BALSA", "BALSA"), ("PEDIDO", "PEDIDO"), ("STATUS", "STATUS")
    ]
    
    pdf.set_font("Arial", size=10)
    for label, chave in campos:
        pdf.set_fill_color(240, 240, 240)
        pdf.cell(50, 7, txt=f" {label}:", border=1, fill=True)
        texto = str(dados.get(chave, '---')).encode('latin-1', 'replace').decode('latin-1')
        pdf.cell(140, 7, txt=f" {texto}", border=1); pdf.ln()
    
    pdf.ln(5); pdf.set_font("Arial", 'B', 10); pdf.cell(0, 8, "DESCRIÇÃO:", ln=True)
    pdf.set_font("Arial", size=10); pdf.multi_cell(0, 7, txt=str(dados.get('DESCRIÇÃO', '---')), border=1)
    return pdf.output(dest='S').encode('latin-1', 'ignore')

# --- SIDEBAR ---
with st.sidebar:
    if os.path.exists("LOGO.PNG"):
        if st.button("🏠 MENU PRINCIPAL"): st.session_state.tela = "MENU_ICONES"; st.rerun()
        st.image("LOGO.PNG", use_container_width=True)

# --- TELAS ---

if st.session_state.tela == "HOME":
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if os.path.exists("LOGO.PNG"): st.image("LOGO.PNG", use_container_width=True)
        if st.button("🔵 ENTRAR NO SISTEMA", use_container_width=True): st.session_state.tela = "MENU_ICONES"; st.rerun()

elif st.session_state.tela == "MENU_ICONES":
    st.markdown("<h2 style='text-align: center;'>PAINEL DE GESTÃO</h2>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    if c1.button("⏳ AGENDAMENTO", use_container_width=True): st.session_state.tela = "AGENDAMENTO"; st.rerun()
    if c2.button("💰 FINANCEIRO", use_container_width=True): st.session_state.tela = "FINANCEIRO"; st.rerun()

elif st.session_state.tela == "AGENDAMENTO":
    # Dashboard de Indicadores
    if st.session_state.db_os:
        df_d = pd.DataFrame(st.session_state.db_os)
        a = len(df_d[df_d['STATUS'].str.contains("ANDAMENTO")])
        f = len(df_d[df_d['STATUS'].str.contains("ENCERRADO")])
        m1, m2, m3 = st.columns(3)
        m1.metric("O.S. EM ANDAMENTO", a)
        m2.metric("O.S. ENCERRADAS", f)
        m3.metric("TOTAL DE OPERAÇÕES", len(df_d))

    if st.button("🔴 NOVO CADASTRO"):
        st.session_state.exibir_form = not st.session_state.exibir_form

    if st.session_state.exibir_form:
        with st.form("f_cadastro", clear_on_submit=True):
            st.subheader("📝 Detalhes da Ordem de Serviço")
            c1, c2, c3, c4 = st.columns(4)
            os_n = c1.text_input("Nº O.S")
            ped = c2.text_input("PEDIDO")
            cli = c3.text_input("CLIENTE", value="TRANSDOURADA")
            tipo = c4.selectbox("TIPO SERVIÇO", ["ESCOLTA", "VIGILANTE"])
            
            c5, c6, c7, c8 = st.columns(4)
            ini = c5.date_input("INÍCIO MISSÃO", format="DD/MM/YYYY")
            fim = c6.date_input("FIM MISSÃO", format="DD/MM/YYYY")
            h_emb = c7.text_input("HORA EMBARQUE")
            sai = c8.text_input("SAÍDA")
            
            c9, c10, c11, c12 = st.columns(4)
            emp = c9.text_input("EMPURRADOR")
            cmt = c10.text_input("CMT")
            esc1 = c11.text_input("ESCOLTA 1")
            esc2 = c12.text_input("ESCOLTA 2")
            
            c13, c14, c15, c16 = st.columns(4)
            ori = c13.text_input("LOCAL ORIGEM")
            dst = c14.text_input("DESTINO")
            bal = c15.text_input("BALSA")
            stt = c16.selectbox("STATUS", ["ANDAMENTO", "ENCERRADO"])
            
            desc = st.text_area("DESCRIÇÃO COMPLETA")
            ass = st.text_input("ASSINATURA")

            if st.form_submit_button("✅ SALVAR OPERAÇÃO"):
                dias = (fim - ini).days if (fim - ini).days > 0 else 1
                valor_dia = 1870.0 if tipo == "ESCOLTA" else 970.0
                st.session_state.db_os.append({
                    "O.S": os_n, "PEDIDO": ped, "CLIENTE": cli, "TIPO": tipo,
                    "INICIO": ini.strftime('%d/%m/%Y'), "FIM": fim.strftime('%d/%m/%Y'),
                    "HORA": h_emb, "SAIDA": sai, "EMPURRADOR": emp, "CMT": cmt,
                    "ESCOLTA1": esc1, "ESCOLTA2": esc2, "LOCAL": ori, "DESTINO": dst,
                    "BALSA": bal, "STATUS": "⏳ ANDAMENTO" if stt == "ANDAMENTO" else "✅ ENCERRADO",
                    "DESCRIÇÃO": desc, "ASSINATURA": ass, "DIAS": dias, "TOTAL": dias * valor_dia, "DT_OBJ": ini
                })
                st.session_state.exibir_form = False; st.rerun()

    if st.session_state.db_os:
        df = pd.DataFrame(st.session_state.db_os)
        # Tabela com TODOS os campos visíveis conforme solicitado
        colunas_vistas = ["O.S", "PEDIDO", "CLIENTE", "TIPO", "INICIO", "FIM", "DIAS", "EMPURRADOR", "CMT", "ESCOLTA1", "ESCOLTA2", "LOCAL", "DESTINO", "BALSA", "STATUS"]
        st.dataframe(df[colunas_vistas], use_container_width=True, hide_index=True)
        
        for i, row in df.iterrows():
            with st.expander(f"⚙️ AÇÕES O.S {row['O.S']}"):
                c_ed, c_pr = st.columns(2)
                if c_ed.button(f"🟠 EDITAR O.S {row['O.S']}", key=f"ed_{i}"):
                    st.session_state.editando_idx = i; st.session_state.tela = "EDITAR"; st.rerun()
                pdf_b = gerar_pdf_os(row.to_dict())
                c_pr.download_button(f"📥 BAIXAR PDF", data=pdf_b, file_name=f"OS_{row['O.S']}.pdf", key=f"pdf_{i}")

elif st.session_state.tela == "FINANCEIRO":
    st.title("💰 Consolidação Financeira")
    if st.session_state.db_os:
        df_f = pd.DataFrame(st.session_state.db_os)
        df_f['VALOR_TOTAL'] = df_f.apply(lambda x: f"R$ {x['TOTAL']:,.2f}" if "ENCERRADO" in x['STATUS'] else "AGUARDANDO FIM", axis=1)
        st.table(df_f[["O.S", "CLIENTE", "TIPO", "DIAS", "STATUS", "VALOR_TOTAL"]])

elif st.session_state.tela == "EDITAR":
    idx = st.session_state.editando_idx
    if idx is not None:
        st.title(f"🟠 Editar O.S {st.session_state.db_os[idx]['O.S']}")
        with st.form("f_ed"):
            n_stt = st.selectbox("STATUS", ["ANDAMENTO", "ENCERRADO"], index=0 if "ANDAMENTO" in st.session_state.db_os[idx]['STATUS'] else 1)
            n_desc = st.text_area("DESCRIÇÃO", value=st.session_state.db_os[idx]['DESCRIÇÃO'])
            if st.form_submit_button("💾 SALVAR ALTERAÇÕES"):
                st.session_state.db_os[idx]['STATUS'] = "⏳ ANDAMENTO" if n_stt == "ANDAMENTO" else "✅ ENCERRADO"
                st.session_state.db_os[idx]['DESCRIÇÃO'] = n_desc
                st.session_state.tela = "AGENDAMENTO"; st.rerun()
        if st.button("❌ CANCELAR"): st.session_state.tela = "AGENDAMENTO"; st.rerun()
