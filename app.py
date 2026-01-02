import streamlit as st
import pandas as pd
from fpdf import FPDF
import os
from datetime import datetime

# Configuração da Página
st.set_page_config(page_title="ZION TECNOLOGIA", layout="wide")

# Inicialização do Banco
if 'db_os' not in st.session_state: st.session_state.db_os = []
if 'tela' not in st.session_state: st.session_state.tela = "HOME"
if 'editando_idx' not in st.session_state: st.session_state.editando_idx = None

# --- FUNÇÃO GERADORA DE PDF O.S ---
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
    campos = [("INÍCIO", "INICIO"), ("FIM", "FIM"), ("EMPURRADOR", "EMPURRADOR"), ("CMT", "CMT"), ("STATUS", "STATUS")]
    pdf.set_font("Arial", size=10)
    for label, chave in campos:
        pdf.cell(50, 7, txt=f" {label}:", border=1)
        pdf.cell(140, 7, txt=f" {str(dados.get(chave, '---'))}", border=1); pdf.ln()
    return pdf.output(dest='S').encode('latin-1', 'ignore')

# --- FUNÇÃO RELATÓRIO FINANCEIRO PDF ---
def gerar_relatorio_financeiro(df_periodo, data_i, data_f):
    pdf = FPDF(orientation='L', unit='mm', format='A4')
    pdf.add_page()
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, f"RELATÓRIO FINANCEIRO - {data_i.strftime('%d/%m/%Y')} A {data_f.strftime('%d/%m/%Y')}", ln=True, align='C')
    pdf.ln(10)
    # Cabeçalho da Tabela
    pdf.set_font("Arial", 'B', 10)
    pdf.set_fill_color(200, 200, 200)
    pdf.cell(20, 8, "O.S", 1, 0, 'C', True)
    pdf.cell(60, 8, "CLIENTE", 1, 0, 'C', True)
    pdf.cell(30, 8, "INICIO", 1, 0, 'C', True)
    pdf.cell(30, 8, "FIM", 1, 0, 'C', True)
    pdf.cell(20, 8, "DIAS", 1, 0, 'C', True)
    pdf.cell(40, 8, "TIPO", 1, 0, 'C', True)
    pdf.cell(40, 8, "TOTAL", 1, 1, 'C', True)
    
    pdf.set_font("Arial", size=10)
    total_geral = 0
    for _, row in df_periodo.iterrows():
        # Somente soma e exibe valor se encerrado
        valor_str = f"R$ {row['TOTAL']:,.2f}" if "ENCERRADO" in str(row['STATUS']) else "R$ 0,00"
        if "ENCERRADO" in str(row['STATUS']): total_geral += row['TOTAL']
        
        pdf.cell(20, 8, str(row['O.S']), 1)
        pdf.cell(60, 8, str(row['CLIENTE'])[:25], 1)
        pdf.cell(30, 8, str(row['INICIO']), 1)
        pdf.cell(30, 8, str(row['FIM']), 1)
        pdf.cell(20, 8, str(row['DIAS']), 1)
        pdf.cell(40, 8, str(row['TIPO']), 1)
        pdf.cell(40, 8, valor_str, 1, 1)
    
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, f"TOTAL DO PERÍODO: R$ {total_geral:,.2f}", 0, 1, 'R')
    return pdf.output(dest='S').encode('latin-1', 'ignore')

# --- TELAS ---
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
    if st.button("⬅️ VOLTAR"): st.session_state.tela = "MENU_ICONES"; st.rerun()
    st.title("⏳ Agendamento e Cadastro")
    with st.expander("➕ NOVO CADASTRO"):
        with st.form("f_cadastro", clear_on_submit=True):
            c1, c2, c3 = st.columns(3)
            cli = c1.text_input("CLIENTE", value="TRANSDOURADA")
            tipo = c1.selectbox("TIPO", ["ESCOLTA", "VIGILANTE"])
            os_n = c1.text_input("O.S")
            ini = c2.date_input("INÍCIO", format="DD/MM/YYYY")
            fim = c2.date_input("FIM", format="DD/MM/YYYY")
            emp = c2.text_input("EMPURRADOR")
            cmt = c3.text_input("CMT")
            stt = c3.selectbox("STATUS", ["ANDAMENTO", "ENCERRADO"])
            r1, r2, r3 = st.columns(3)
            ori, dest, bal = r1.text_input("LOCAL"), r2.text_input("DESTINO"), r3.text_input("BALSA")
            desc = st.text_area("DESCRIÇÃO")
            if st.form_submit_button("✅ SALVAR"):
                dias = (fim - ini).days if (fim - ini).days > 0 else 1
                v_diaria = 1870.0 if tipo == "ESCOLTA" else 970.0
                st.session_state.db_os.append({
                    "O.S": os_n, "INICIO": ini.strftime('%d/%m/%Y'), "FIM": fim.strftime('%d/%m/%Y'),
                    "DT_OBJ": ini, "DIAS": dias, "TIPO": tipo, "VALOR_DIARIA": v_diaria, "TOTAL": dias * v_diaria,
                    "EMPURRADOR": emp, "CMT": cmt, "CLIENTE": cli, "BALSA": bal, "STATUS": "✅ ENCERRADO" if stt == "ENCERRADO" else "⏳ ANDAMENTO", "DESCRIÇÃO": desc
                })
                st.rerun()
    if st.session_state.db_os:
        st.dataframe(pd.DataFrame(st.session_state.db_os).drop(columns=['DT_OBJ']), use_container_width=True)

elif st.session_state.tela == "FINANCEIRO":
    if st.button("⬅️ VOLTAR"): st.session_state.tela = "MENU_ICONES"; st.rerun()
    st.title("💰 Financeiro")
    
    if st.session_state.db_os:
        df_f = pd.DataFrame(st.session_state.db_os)
        
        # Filtro de Período para o Relatório
        st.markdown("### 📅 Gerar Relatório por Período")
        col_d1, col_d2, col_btn = st.columns([2, 2, 2])
        data_inicio = col_d1.date_input("Data Inicial", datetime.now())
        data_final = col_d2.date_input("Data Final", datetime.now())
        
        # Filtragem dos dados
        df_filtrado = df_f[(df_f['DT_OBJ'] >= data_inicio) & (df_f['DT_OBJ'] <= data_final)]
        
        # BOTÃO AZUL PARA PDF
        pdf_relatorio = gerar_relatorio_financeiro(df_filtrado, data_inicio, data_final)
        col_btn.markdown("<br>", unsafe_allow_html=True)
        col_btn.download_button(
            label="🔵 GERAR RELATÓRIO PDF",
            data=pdf_relatorio,
            file_name=f"Relatorio_Zion_{data_inicio}.pdf",
            mime="application/pdf",
            use_container_width=True
        )

        st.divider()
        st.write("### 💵 Detalhamento por Operação")
        # Criar exibição onde valor só aparece se encerrado
        df_display = df_f.copy()
        df_display['VALOR EXIBIDO'] = df_display.apply(lambda x: f"R$ {x['TOTAL']:,.2f}" if "ENCERRADO" in x['STATUS'] else "---", axis=1)
        
        st.table(df_display[["O.S", "CLIENTE", "INICIO", "FIM", "STATUS", "VALOR EXIBIDO"]])
        
        total_encerrado = df_f[df_f['STATUS'].str.contains("ENCERRADO")]['TOTAL'].sum()
        st.metric("TOTAL RECEBÍVEL (ENCERRADOS)", f"R$ {total_encerrado:,.2f}")
    else:
        st.info("Nenhuma O.S cadastrada.")
