import streamlit as st
import pandas as pd
from fpdf import FPDF
import os
from datetime import datetime

# Configuração da Página
st.set_page_config(page_title="ZION TECNOLOGIA", layout="wide")

# Estilização CSS para a Tabela estilo Dark do Vídeo
st.markdown("""
    <style>
    .stDataFrame { border-radius: 10px; }
    div[data-testid="stExpander"] { border: 1px solid #ff4b4b; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# Inicialização do Banco
if 'db_os' not in st.session_state: st.session_state.db_os = []
if 'tela' not in st.session_state: st.session_state.tela = "HOME"
if 'editando_idx' not in st.session_state: st.session_state.editando_idx = None

# --- GERADOR DE PDF ---
def gerar_pdf_zion(dados):
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.add_page()
    logo_cliente = "logo app.jpg"
    if os.path.exists(logo_cliente):
        try: pdf.image(logo_cliente, x=65, y=10, w=80); pdf.ln(30)
        except: pdf.ln(10)
    else: pdf.ln(10)

    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "ORDEM DE SERVIÇO DE ESCOLTA", ln=True, align='C')
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(0, 7, f"CLIENTE: {str(dados.get('CLIENTE', '---'))}", ln=True, align='C')
    pdf.cell(0, 7, f"O.S Nº: {str(dados.get('O.S', '---'))} | PEDIDO: {str(dados.get('PEDIDO', '---'))}", ln=True, align='C')
    pdf.ln(5); pdf.line(10, pdf.get_y(), 200, pdf.get_y()); pdf.ln(5)
    
    campos = [
        ("INÍCIO DA MISSÃO", "INICIO"), ("HORA EMBARQUE", "HORA"),
        ("FIM DA MISSÃO", "FIM"), ("LOCAL", "LOCAL"),
        ("EMPURRADOR", "EMPURRADOR"), ("CMT", "CMT"),
        ("SAÍDA", "SAIDA"), ("DESTINO", "DESTINO"),
        ("BALSAS", "BALSA"), ("ESCOLTA 1", "ESCOLTA1"),
        ("ESCOLTA 2", "ESCOLTA2"), ("STATUS", "STATUS")
    ]
    
    pdf.set_font("Arial", size=10)
    for label, chave in campos:
        pdf.set_fill_color(245, 245, 245)
        pdf.set_font("Arial", 'B', 10)
        pdf.cell(50, 7, txt=f" {label}:", border=1, fill=True)
        pdf.set_font("Arial", size=10)
        pdf.cell(140, 7, txt=f" {str(dados.get(chave, '---'))}", border=1); pdf.ln()

    pdf.ln(5); pdf.set_font("Arial", 'B', 10); pdf.cell(0, 8, "DETALHAMENTO DA MISSÃO:", ln=True)
    pdf.set_font("Arial", size=10); pdf.multi_cell(0, 7, txt=str(dados.get('DESCRIÇÃO', '---')), border=1)

    pdf.ln(25)
    pdf.cell(95, 10, "__________________________", 0, 0, 'C')
    pdf.cell(95, 10, "__________________________", 0, 1, 'C')
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(95, 5, "SOLICITANTE", 0, 0, 'C')
    pdf.cell(95, 5, "RESPONSÁVEL CLIENTE", 0, 1, 'C')
    
    return pdf.output(dest='S').encode('latin-1', 'ignore')

# --- NAVEGAÇÃO ---
with st.sidebar:
    if os.path.exists("LOGO.PNG"):
        if st.button("🏠 MENU PRINCIPAL", use_container_width=True):
            st.session_state.tela = "MENU_ICONES"; st.rerun()
        st.image("LOGO.PNG", use_container_width=True)

if st.session_state.tela == "HOME":
    st.markdown("<h1 style='text-align: center;'>ZION TECNOLOGIA</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if os.path.exists("LOGO.PNG"): st.image("LOGO.PNG")
        if st.button("🔵 ACESSAR SISTEMA", use_container_width=True):
            st.session_state.tela = "MENU_ICONES"; st.rerun()

elif st.session_state.tela == "MENU_ICONES":
    st.markdown("<h2 style='text-align: center;'>PAINEL DE GESTÃO</h2>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("⏳ AGENDAMENTO & CADASTRO", use_container_width=True): st.session_state.tela = "AGENDAMENTO"; st.rerun()
    with c2:
        if st.button("💰 FINANCEIRO", use_container_width=True): st.session_state.tela = "FINANCEIRO"; st.rerun()

elif st.session_state.tela == "AGENDAMENTO":
    if st.button("⬅️ VOLTAR AO PAINEL"): st.session_state.tela = "MENU_ICONES"; st.rerun()
    
    st.title("⏳ Agendamento e Novo Cadastro")
    
    with st.expander("➕ NOVO CADASTRO", expanded=False):
        with st.form("f_cadastro", clear_on_submit=True):
            c1, c2, c3 = st.columns(3)
            with c1:
                cli = st.text_input("CLIENTE", value="TRANSDOURADA")
                tipo = st.selectbox("TIPO SERVIÇO", ["ESCOLTA", "VIGILANTE"])
                ped = st.text_input("PEDIDO")
                os_n = st.text_input("O.S")
            with c2:
                ini = st.date_input("INÍCIO MISSÃO", format="DD/MM/YYYY")
                fim = st.date_input("FIM MISSÃO", format="DD/MM/YYYY")
                h_emb = st.text_input("HORA EMBARQUE")
                emp = st.text_input("EMPURRADOR")
            with c3:
                cmt = st.text_input("CMT")
                esc1 = st.text_input("ESCOLTA 1")
                esc2 = st.text_input("ESCOLTA 2")
                stt = st.selectbox("STATUS", ["ANDAMENTO", "ENCERRADO"])
            
            # Campos Retangulares Pequenos
            r1, r2, r3 = st.columns(3)
            ori = r1.text_input("LOCAL")
            dest = r2.text_input("DESTINO")
            bal = r3.text_input("BALSA")
            
            desc = st.text_area("DESCRIÇÃO")
            ass = st.text_input("ASSINATURA (NOME)")

            if st.form_submit_button("✅ SALVAR"):
                dias = (fim - ini).days if (fim - ini).days > 0 else 1
                v_diaria = 1870.0 if tipo == "ESCOLTA" else 970.0
                st.session_state.db_os.append({
                    "O.S": os_n, "INICIO": ini.strftime('%d/%m/%Y'), "FIM": fim.strftime('%d/%m/%Y'),
                    "HORA": h_emb, "LOCAL": ori, "EMPURRADOR": emp, "CMT": cmt, "SAIDA": ori,
                    "ESCOLTA1": esc1, "ESCOLTA2": esc2, "DESCRIÇÃO": desc, "ASSINATURA": f"🖋️ {ass}",
                    "CLIENTE": cli, "BALSA": bal, "DESTINO": dest, "PEDIDO": ped, 
                    "STATUS": "✅ ENCERRADO" if stt == "ENCERRADO" else "⏳ ANDAMENTO",
                    "DIAS": dias, "TIPO": tipo, "TOTAL": dias * v_diaria
                })
                st.success("Salvo!")
                st.rerun()

    st.divider()
    
    # EXIBIÇÃO ESTILO VÍDEO (TABELA COMPLETA)
    if st.session_state.db_os:
        df = pd.DataFrame(st.session_state.db_os)
        cols = ["O.S", "INICIO", "HORA", "LOCAL", "EMPURRADOR", "CMT", "SAIDA", "FIM", "ESCOLTA1", "ESCOLTA2", "DESCRIÇÃO", "ASSINATURA", "CLIENTE", "BALSA", "DESTINO", "PEDIDO", "STATUS"]
        st.write("### 📋 Registros de Operações")
        st.dataframe(df[cols], use_container_width=True, hide_index=True)
        
        for i, row in df.iterrows():
            with st.expander(f"OPÇÕES O.S {row['O.S']} - {row['EMPURRADOR']}"):
                col_a, col_b = st.columns(2)
                if col_a.button(f"🟠 EDITAR", key=f"ed_{i}"):
                    st.session_state.editando_idx = i; st.session_state.tela = "EDITAR"; st.rerun()
                pdf = gerar_pdf_zion(row.to_dict())
                col_b.download_button(f"📥 BAIXAR PDF", data=pdf, file_name=f"OS_{row['O.S']}.pdf", key=f"pdf_{i}")

elif st.session_state.tela == "FINANCEIRO":
    if st.button("⬅️ VOLTAR"): st.session_state.tela = "MENU_ICONES"; st.rerun()
    st.title("💰 Financeiro Zion")
    if st.session_state.db_os:
        df_f = pd.DataFrame(st.session_state.db_os)
        st.table(df_f[["O.S", "CLIENTE", "TIPO", "DIAS", "TOTAL", "STATUS"]])
        st.metric("FATURAMENTO TOTAL", f"R$ {df_f['TOTAL'].sum():,.2f}")

elif st.session_state.tela == "EDITAR":
    idx = st.session_state.editando_idx
    if idx is not None:
        st.title(f"🟠 Editar O.S {st.session_state.db_os[idx]['O.S']}")
        with st.form("f_ed"):
            ed_stt = st.selectbox("STATUS", ["ANDAMENTO", "ENCERRADO"])
            ed_desc = st.text_area("DESCRIÇÃO", value=st.session_state.db_os[idx]['DESCRIÇÃO'])
            if st.form_submit_button("💾 SALVAR"):
                st.session_state.db_os[idx]['STATUS'] = "✅ ENCERRADO" if ed_stt == "ENCERRADO" else "⏳ ANDAMENTO"
                st.session_state.db_os[idx]['DESCRIÇÃO'] = ed_desc
                st.session_state.tela = "AGENDAMENTO"; st.rerun()
        if st.button("❌ CANCELAR"): st.session_state.tela = "AGENDAMENTO"; st.rerun()
