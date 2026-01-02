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
    # Logo no PDF (logo app.jpg conforme solicitado anteriormente)
    logo_pdf = "logo app.jpg"
    if os.path.exists(logo_pdf):
        try: pdf.image(logo_pdf, x=10, y=10, w=50)
        except: pass
    
    pdf.set_font("Arial", 'B', 14)
    pdf.ln(20)
    pdf.cell(0, 10, "ORDEM DE SERVIÇO DE ESCOLTA", ln=True, align='C')
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(0, 7, f"CLIENTE: {str(dados.get('CLIENTE', '---'))}", ln=True, align='C')
    pdf.cell(0, 7, f"O.S Nº: {str(dados.get('O.S', '---'))} | PEDIDO: {str(dados.get('PEDIDO', '---'))}", ln=True, align='C')
    pdf.ln(5); pdf.line(10, pdf.get_y(), 200, pdf.get_y()); pdf.ln(5)
    
    campos = [
        ("INÍCIO DA MISSÃO", "INICIO"), ("HORA EMBARQUE", "HORA"),
        ("FIM DA MISSÃO", "FIM"), ("LOCAL", "LOCAL"),
        ("EMPURRADOR", "EMPURRADOR"), ("CMT", "CMT"),
        ("BALSAS", "BALSA"), ("DESTINO", "DESTINO"), ("STATUS", "STATUS")
    ]
    
    pdf.set_font("Arial", size=10)
    for label, chave in campos:
        pdf.set_fill_color(245, 245, 245)
        pdf.cell(50, 7, txt=f" {label}:", border=1, fill=True)
        pdf.cell(140, 7, txt=f" {str(dados.get(chave, '---'))}", border=1); pdf.ln()

    pdf.ln(5); pdf.set_font("Arial", 'B', 10); pdf.cell(0, 8, "DETALHAMENTO DA MISSÃO:", ln=True)
    pdf.set_font("Arial", size=10); pdf.multi_cell(0, 7, txt=str(dados.get('DESCRIÇÃO', '---')), border=1)

    pdf.ln(25); pdf.cell(95, 10, "__________________________", 0, 0, 'C'); pdf.cell(95, 10, "__________________________", 0, 1, 'C')
    pdf.cell(95, 5, "ZION TECNOLOGIA", 0, 0, 'C'); pdf.cell(95, 5, "RESPONSÁVEL CLIENTE", 0, 1, 'C')
    return pdf.output(dest='S').encode('latin-1', 'ignore')

# --- SIDEBAR NAVEGÁVEL COM LOGO ---
with st.sidebar:
    if os.path.exists("LOGO.PNG"):
        # Logo clicável para retornar ao painel
        if st.button("🏠 RETORNAR AO PAINEL", use_container_width=True):
            st.session_state.tela = "MENU_ICONES"
            st.rerun()
        st.image("LOGO.PNG", use_container_width=True)
    st.divider()

# --- TELAS ---

# TELA HOME (LOGO CENTRALIZADA)
if st.session_state.tela == "HOME":
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if os.path.exists("LOGO.PNG"):
            st.image("LOGO.PNG", use_container_width=True)
        st.markdown("<h1 style='text-align: center;'>CONTROLE DE VIGILÂNCIA</h1>", unsafe_allow_html=True)
        if st.button("🔵 ACESSAR SISTEMA", use_container_width=True):
            st.session_state.tela = "MENU_ICONES"
            st.rerun()

# PAINEL DE GESTÃO (ÍCONES)
elif st.session_state.tela == "MENU_ICONES":
    st.markdown("<h2 style='text-align: center;'>PAINEL DE GESTÃO</h2>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    if c1.button("⏳ AGENDAMENTO", use_container_width=True): 
        st.session_state.tela = "AGENDAMENTO"; st.rerun()
    if c2.button("💰 FINANCEIRO", use_container_width=True): 
        st.session_state.tela = "FINANCEIRO"; st.rerun()
    if c3.button("📝 NOVO CADASTRO", use_container_width=True): 
        st.session_state.tela = "AGENDAMENTO"; st.rerun()

# AGENDAMENTO E CADASTRO
elif st.session_state.tela == "AGENDAMENTO":
    st.title("⏳ Agendamento e Cadastro")
    
    with st.expander("➕ NOVO CADASTRO", expanded=False):
        with st.form("f_cadastro", clear_on_submit=True):
            c1, c2, c3 = st.columns(3)
            cli = c1.text_input("CLIENTE", value="TRANSDOURADA")
            tipo = c1.selectbox("TIPO SERVIÇO", ["ESCOLTA", "VIGILANTE"])
            os_n = c1.text_input("O.S")
            
            ini = c2.date_input("INÍCIO MISSÃO", format="DD/MM/YYYY")
            fim = c2.date_input("FIM MISSÃO", format="DD/MM/YYYY")
            h_emb = c2.text_input("HORA EMBARQUE")
            
            emp = c3.text_input("EMPURRADOR")
            cmt = c3.text_input("CMT")
            stt = c3.selectbox("STATUS", ["ANDAMENTO", "ENCERRADO"])
            
            # Campos Retangulares (Local, Destino, Balsa)
            r1, r2, r3 = st.columns(3)
            ori, dest, bal = r1.text_input("LOCAL"), r2.text_input("DESTINO"), r3.text_input("BALSA")
            
            desc = st.text_area("DESCRIÇÃO")
            ass_n = st.text_input("ASSINATURA")

            if st.form_submit_button("✅ SALVAR"):
                dias = (fim - ini).days if (fim - ini).days > 0 else 1
                v_diaria = 1870.0 if tipo == "ESCOLTA" else 970.0
                st.session_state.db_os.append({
                    "O.S": os_n, "INICIO": ini.strftime('%d/%m/%Y'), "FIM": fim.strftime('%d/%m/%Y'),
                    "DT_OBJ": ini, "DIAS": dias, "TIPO": tipo, "TOTAL": dias * v_diaria,
                    "HORA": h_emb, "LOCAL": ori, "EMPURRADOR": emp, "CMT": cmt, "CLIENTE": cli, 
                    "BALSA": bal, "DESTINO": dest, "PEDIDO": "0001", 
                    "STATUS": "⏳ ANDAMENTO" if stt == "ANDAMENTO" else "✅ ENCERRADO",
                    "DESCRIÇÃO": desc, "ASSINATURA": ass_n
                })
                st.success("Cadastro Realizado com Sucesso!")
                st.rerun()

    if st.session_state.db_os:
        df = pd.DataFrame(st.session_state.db_os)
        # Removido Valor Diária da visão de agendamento
        cols_agend = ["O.S", "INICIO", "FIM", "DIAS", "TIPO", "EMPURRADOR", "CMT", "CLIENTE", "STATUS"]
        st.dataframe(df[cols_agend], use_container_width=True, hide_index=True)
        
        for i, row in df.iterrows():
            with st.expander(f"AÇÕES O.S {row['O.S']}"):
                col_ed, col_pr = st.columns(2)
                if col_ed.button(f"🟠 EDITAR O.S {row['O.S']}", key=f"ed_{i}"):
                    st.session_state.editando_idx = i; st.session_state.tela = "EDITAR"; st.rerun()
                
                pdf_bytes = gerar_pdf_os(row.to_dict())
                col_pr.download_button(f"📥 IMPRIMIR O.S {row['O.S']}", data=pdf_bytes, file_name=f"OS_{row['O.S']}.pdf", key=f"pdf_{i}")

# FINANCEIRO
elif st.session_state.tela == "FINANCEIRO":
    st.title("💰 Financeiro")
    if st.session_state.db_os:
        df_f = pd.DataFrame(st.session_state.db_os)
        
        # Filtro e Botão Azul de Relatório
        c_i, c_f, c_b = st.columns([2, 2, 2])
        d_ini = c_i.date_input("De:", datetime.now())
        d_fim = c_f.date_input("Até:", datetime.now())
        
        c_b.markdown("<br>", unsafe_allow_html=True)
        if c_b.button("🔵 GERAR RELATÓRIO PDF", use_container_width=True):
            st.info("Função de download do relatório consolidado disponível no botão azul acima.")

        # Lógica: Valor só aparece se status for ENCERRADO
        df_f['VALOR EXIBIDO'] = df_f.apply(lambda x: f"R$ {x['TOTAL']:,.2f}" if "ENCERRADO" in x['STATUS'] else "---", axis=1)
        st.table(df_f[["O.S", "CLIENTE", "STATUS
