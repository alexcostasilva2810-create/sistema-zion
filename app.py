import streamlit as st
import pandas as pd
from fpdf import FPDF
import os
from datetime import datetime

# Configuração da Página
st.set_page_config(page_title="ZION TECNOLOGIA", layout="wide")

# Inicialização do Banco de Dados
if 'db_os' not in st.session_state: st.session_state.db_os = []
if 'tela' not in st.session_state: st.session_state.tela = "HOME"
if 'editando_idx' not in st.session_state: st.session_state.editando_idx = None

# --- FUNÇÃO GERADORA DE PDF O.S ---
def gerar_pdf_os(dados):
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.add_page()
    # Tenta carregar a logo do cliente para o PDF
    logo_pdf = "logo app.jpg"
    if os.path.exists(logo_pdf):
        try: pdf.image(logo_pdf, x=10, y=10, w=45)
        except: pass
    
    pdf.set_font("Arial", 'B', 14)
    pdf.ln(20)
    pdf.cell(0, 10, "ORDEM DE SERVIÇO DE ESCOLTA", ln=True, align='C')
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(0, 7, f"CLIENTE: {str(dados.get('CLIENTE', '---'))} | O.S Nº: {str(dados.get('O.S', '---'))}", ln=True, align='C')
    pdf.ln(5); pdf.line(10, pdf.get_y(), 200, pdf.get_y()); pdf.ln(5)
    
    campos = [
        ("INÍCIO", "INICIO"), ("FIM", "FIM"), ("EMPURRADOR", "EMPURRADOR"),
        ("CMT", "CMT"), ("LOCAL", "LOCAL"), ("DESTINO", "DESTINO"), 
        ("BALSAS", "BALSA"), ("STATUS", "STATUS")
    ]
    
    pdf.set_font("Arial", size=10)
    for label, chave in campos:
        pdf.set_fill_color(240, 240, 240)
        pdf.cell(50, 7, txt=f" {label}:", border=1, fill=True)
        pdf.cell(140, 7, txt=f" {str(dados.get(chave, '---'))}", border=1); pdf.ln()

    pdf.ln(5); pdf.set_font("Arial", 'B', 10); pdf.cell(0, 8, "DETALHAMENTO:", ln=True)
    pdf.set_font("Arial", size=10); pdf.multi_cell(0, 7, txt=str(dados.get('DESCRIÇÃO', '---')), border=1)
    
    return pdf.output(dest='S').encode('latin-1', 'ignore')

# --- FUNÇÃO RELATÓRIO FINANCEIROConsolidado ---
def gerar_relatorio_financeiro(df_periodo, data_i, data_f):
    pdf = FPDF(orientation='L', unit='mm', format='A4')
    pdf.add_page()
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, f"RELATÓRIO FINANCEIRO ZION: {data_i.strftime('%d/%m/%Y')} - {data_f.strftime('%d/%m/%Y')}", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 9)
    headers = [("O.S", 20), ("CLIENTE", 70), ("INICIO", 35), ("FIM", 35), ("TOTAL", 40)]
    for h, w in headers: pdf.cell(w, 8, h, 1, 0, 'C', True)
    pdf.ln()
    
    pdf.set_font("Arial", size=9)
    total_faturado = 0
    for _, row in df_periodo.iterrows():
        is_encerrado = "ENCERRADO" in str(row['STATUS']).upper()
        valor = row['TOTAL'] if is_encerrado else 0
        total_faturado += valor
        pdf.cell(20, 8, str(row['O.S']), 1)
        pdf.cell(70, 8, str(row['CLIENTE']), 1)
        pdf.cell(35, 8, str(row['INICIO']), 1)
        pdf.cell(35, 8, str(row['FIM']), 1)
        pdf.cell(40, 8, f"R$ {valor:,.2f}", 1, 1)
    
    pdf.ln(5); pdf.set_font("Arial", 'B', 11)
    pdf.cell(0, 10, f"VALOR TOTAL RECEBÍVEL: R$ {total_faturado:,.2f}", 0, 1, 'R')
    return pdf.output(dest='S').encode('latin-1', 'ignore')

# --- NAVEGAÇÃO / SIDEBAR ---
with st.sidebar:
    if os.path.exists("LOGO.PNG"):
        if st.button("🏠 VOLTAR AO MENU", use_container_width=True):
            st.session_state.tela = "MENU_ICONES"
            st.rerun()
        st.image("LOGO.PNG", use_container_width=True)
    st.divider()
    if st.button("📊 RESUMO FINANCEIRO", use_container_width=True):
        st.session_state.tela = "FINANCEIRO"
        st.rerun()

# --- TELAS ---

# 1. TELA HOME
if st.session_state.tela == "HOME":
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if os.path.exists("LOGO.PNG"):
            st.image("LOGO.PNG", use_container_width=True)
        st.markdown("<h2 style='text-align: center;'>SISTEMA DE GESTÃO ZION</h2>", unsafe_allow_html=True)
        if st.button("🔵 ENTRAR NO SISTEMA", use_container_width=True):
            st.session_state.tela = "MENU_ICONES"; st.rerun()

# 2. MENU PRINCIPAL
elif st.session_state.tela == "MENU_ICONES":
    st.markdown("<h2 style='text-align: center;'>PAINEL DE GESTÃO</h2>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    if c1.button("⏳ AGENDAMENTO", use_container_width=True): st.session_state.tela = "AGENDAMENTO"; st.rerun()
    if c2.button("💰 FINANCEIRO", use_container_width=True): st.session_state.tela = "FINANCEIRO"; st.rerun()
    if c3.button("📝 NOVO CADASTRO", use_container_width=True): st.session_state.tela = "AGENDAMENTO"; st.rerun()

# 3. AGENDAMENTO E CADASTRO
elif st.session_state.tela == "AGENDAMENTO":
    st.title("⏳ Agendamento e Cadastro")
    
    with st.expander("➕ REALIZAR NOVO CADASTRO", expanded=False):
        with st.form("f_cadastro", clear_on_submit=True):
            c1, c2, c3 = st.columns(3)
            cli = c1.text_input("CLIENTE", value="TRANSDOURADA")
            tipo = c1.selectbox("TIPO SERVIÇO", ["ESCOLTA", "VIGILANTE"])
            os_n = c1.text_input("Nº O.S")
            
            ini = c2.date_input("DATA INÍCIO", format="DD/MM/YYYY")
            fim = c2.date_input("DATA FIM", format="DD/MM/YYYY")
            h_emb = c2.text_input("HORA EMBARQUE")
            
            emp = c3.text_input("EMPURRADOR")
            cmt = c3.text_input("CMT")
            stt = st.selectbox("STATUS DA MISSÃO", ["ANDAMENTO", "ENCERRADO"])
            
            r1, r2, r3 = st.columns(3)
            ori, dest, bal = r1.text_input("LOCAL ORIGEM"), r2.text_input("DESTINO FINAL"), r3.text_input("BALSAS")
            desc = st.text_area("DETALHAMENTO DA MISSÃO")

            if st.form_submit_button("✅ SALVAR OPERAÇÃO"):
                dias = (fim - ini).days if (fim - ini).days > 0 else 1
                v_diaria = 1870.0 if tipo == "ESCOLTA" else 970.0
                st.session_state.db_os.append({
                    "O.S": os_n, "INICIO": ini.strftime('%d/%m/%Y'), "FIM": fim.strftime('%d/%m/%Y'),
                    "DT_OBJ": ini, "DIAS": dias, "TIPO": tipo, "TOTAL": dias * v_diaria,
                    "HORA": h_emb, "LOCAL": ori, "EMPURRADOR": emp, "CMT": cmt, "CLIENTE": cli, 
                    "BALSA": bal, "DESTINO": dest, "STATUS": "⏳ ANDAMENTO" if stt == "ANDAMENTO" else "✅ ENCERRADO",
                    "DESCRIÇÃO": desc
                })
                st.rerun()

    if st.session_state.db_os:
        df = pd.DataFrame(st.session_state.db_os)
        # Exibição sem Valor Diário conforme pedido
        cols_tab = ["O.S", "INICIO", "FIM", "DIAS", "TIPO", "EMPURRADOR", "CLIENTE", "STATUS"]
        st.dataframe(df[cols_tab], use_container_width=True, hide_index=True)
        
        for i, row in df.iterrows():
            with st.expander(f"OPÇÕES O.S {row['O.S']}"):
                col_ed, col_pr = st.columns(2)
                if col_ed.button(f"🟠 EDITAR", key=f"ed_{i}"):
                    st.session_state.editando_idx = i; st.session_state.tela = "EDITAR"; st.rerun()
                
                pdf_out = gerar_pdf_os(row.to_dict())
                col_pr.download_button(f"📥 IMPRIMIR O.S", data=pdf_out, file_name=f"OS_{row['O.S']}.pdf", key=f"pdf_{i}")

# 4. FINANCEIRO
elif st.session_state.tela == "FINANCEIRO":
    st.title("💰 Controle Financeiro")
    if st.session_state.db_os:
        df_f = pd.DataFrame(st.session_state.db_os)
        
        c_i, c_f, c_b = st.columns([2, 2, 2])
        d_ini = c_i.date_input("Filtrar de:", datetime.now())
        d_fim = c_f.date_input("Filtrar até:", datetime.now())
        
        df_f_filt = df_f
