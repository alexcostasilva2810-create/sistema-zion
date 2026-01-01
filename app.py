import streamlit as st
import pandas as pd
from fpdf import FPDF
import os

# Configuração da Página
st.set_page_config(page_title="ZION TECNOLOGIA", layout="wide")

# Inicialização do Banco de Dados em Memória
if 'db_os' not in st.session_state: st.session_state.db_os = []
if 'tela' not in st.session_state: st.session_state.tela = "HOME"
if 'editando_idx' not in st.session_state: st.session_state.editando_idx = None

# --- FUNÇÃO GERADORA DE PDF A4 (IDENTIDADE TRANSDOURADA) ---
def gerar_pdf_a4_cliente(dados):
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.add_page()
    
    # Nome EXATO do arquivo que você subiu no GitHub
    logo_transdourada = "logo app.jpg" 
    
    if os.path.exists(logo_transdourada):
        try:
            # Ajuste de proporção para a logo da Transdourada
            pdf.image(logo_transdourada, x=55, y=10, w=100) 
            pdf.ln(30)
        except Exception as e:
            pdf.ln(10)
    else:
        pdf.set_font("Arial", 'I', 8)
        pdf.cell(0, 5, "[Logo Transdourada não carregada]", ln=True, align='C')
        pdf.ln(10)

    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "ORDEM DE SERVIÇO DE ESCOLTA", ln=True, align='C')
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(0, 7, f"CLIENTE: {str(dados.get('CLIENTE', 'TRANSDOURADA'))}", ln=True, align='C')
    pdf.cell(0, 7, f"O.S Nº: {str(dados.get('O.S', '---'))} | PEDIDO: {str(dados.get('PEDIDO', '---'))}", ln=True, align='C')
    pdf.ln(5); pdf.line(10, pdf.get_y(), 200, pdf.get_y()); pdf.ln(5)
    
    # Tabela de Dados Operacionais
    pdf.set_font("Arial", size=10)
    ordem_campos = [
        ("INÍCIO DA MISSÃO", "INÍCIO"), ("FIM DA MISSÃO", "FIM"),
        ("EMPURRADOR", "EMPURRADOR"), ("CMT", "CMT"),
        ("LOCAL ORIGEM", "LOCAL (ORIGEM)"), ("SAÍDA DESTINO", "SAÍDA (DESTINO)"),
        ("BALSAS", "BALSAS"), ("STATUS ATUAL", "STATUS")
    ]

    for label, chave in ordem_campos:
        valor = dados.get(chave, "---")
        pdf.set_fill_color(240, 240, 240)
        pdf.set_font("Arial", 'B', 10)
        pdf.cell(50, 8, txt=f" {label}:", border=1, fill=True)
        pdf.set_font("Arial", size=10)
        pdf.cell(140, 8, txt=f" {str(valor)}", border=1); pdf.ln()

    # Descrição
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(0, 8, "DETALHAMENTO DA MISSÃO:", ln=True)
    pdf.set_font("Arial", size=10)
    pdf.multi_cell(0, 7, txt=str(dados.get('DESCRIÇÃO DO SERVIÇO', '---')), border=1)

    # Assinaturas
    pdf.ln(20)
    pdf.cell(95, 10, "__________________________", 0, 0, 'C')
    pdf.cell(95, 10, "__________________________", 0, 1, 'C')
    pdf.set_font("Arial", 'B', 9)
    pdf.cell(95, 5, "ZION TECNOLOGIA", 0, 0, 'C')
    pdf.cell(95, 5, "RESPONSÁVEL CLIENTE", 0, 1, 'C')
    
    return pdf.output(dest='S').encode('latin-1', 'ignore')

# --- NAVEGAÇÃO LATERAL ---
with st.sidebar:
    # Ajuste para sua logo azul da Zion (LOGO.PNG)
    if os.path.exists("LOGO.PNG"):
        if st.button("🏠 MENU PRINCIPAL", use_container_width=True):
            st.session_state.tela = "MENU_ICONES"
            st.rerun()
        st.image("LOGO.PNG", use_container_width=True)
    st.divider()

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
        if st.button("⏳ AGENDAMENTO & CADASTRO", use_container_width=True): 
            st.session_state.tela = "AGENDAMENTO"; st.rerun()
    with c2:
        if st.button("💰 FINANCEIRO", use_container_width=True): 
            st.session_state.tela = "FINANCEIRO"; st.rerun()

elif st.session_state.tela == "AGENDAMENTO":
    if st.button("⬅️ VOLTAR AO PAINEL"):
        st.session_state.tela = "MENU_ICONES"; st.rerun()
    
    st.title("⏳ Agendamento e Novo Cadastro")
    
    with st.expander("➕ CADASTRAR NOVA MISSÃO", expanded=False):
        with st.form("f_cadastro"):
            c1, c2 = st.columns(2)
            with c1:
                cli_n = st.text_input("CLIENTE", value="TRANSDOURADA")
                ped = st.text_input("PEDIDO")
                os_n = st.text_input("O.S Nº")
                d1 = st.date_input("DATA INÍCIO")
            with c2:
                emp = st.text_input("EMPURRADOR")
                cmt = st.text_input("CMT")
                sai_d = st.text_input("DESTINO")
                d2 = st.date_input("DATA FIM")
            
            loc_o = st.text_input("LOCAL ORIGEM")
            bal = st.text_area("BALSAS")
            desc = st.text_area("DESCRIÇÃO / RELATÓRIO")
            stt = st.selectbox("STATUS", ["ANDAMENTO", "ENCERRADO"])

            if st.form_submit_button("✅ SALVAR MISSÃO"):
                dias = (d2 - d1).days if (d2 - d1).days > 0 else 1
                st.session_state.db_os.append({
                    "CLIENTE": cli_n, "PEDIDO": ped, "O.S": os_n, "INÍCIO": d1.strftime('%d/%m/%Y'),
                    "FIM": d2.strftime('%d/%m/%Y'), "LOCAL (ORIGEM)": loc_o, "SAÍDA (DESTINO)": sai_d,
                    "BALSAS": bal, "EMPURRADOR": emp, "CMT": cmt, "DIAS": dias, 
                    "DESCRIÇÃO DO SERVIÇO": desc, "STATUS": stt, 
                    "VALOR_TOTAL": dias * 1870.0
                })
                st.success("Salvo!")
                st.rerun()

    st.divider()
    if st.session_state.db_os:
        df = pd.DataFrame(st.session_state.db_os)
        for i, row in df.iterrows():
            with st.expander(f"O.S {row['O.S']} - {row['EMPURRADOR']}"):
                pdf_b = gerar_pdf_a4_cliente(row.to_dict())
                st.download_button(f"📥 BAIXAR PDF O.S {row['O.S']}", data=pdf_b, 
                                 file_name=f"OS_{row['O.S']}.pdf", key=f"btn_{i}")

elif st.session_state.tela == "FINANCEIRO":
    if st.button("⬅️ VOLTAR AO PAINEL"):
        st.session_state.tela = "MENU_ICONES"; st.rerun()
    st.title("💰 Resumo Financeiro")
    if st.session_state.db_os:
        st.dataframe(pd.DataFrame(st.session_state.db_os), use_container_width=True)
