import streamlit as st
import pandas as pd
from fpdf import FPDF
import os

# Configuração da Página
st.set_page_config(page_title="ZION TECNOLOGIA", layout="wide")

# Inicialização do Banco de Dados
if 'db_os' not in st.session_state: st.session_state.db_os = []
if 'tela' not in st.session_state: st.session_state.tela = "HOME"
if 'editando_idx' not in st.session_state: st.session_state.editando_idx = None

# --- FUNÇÃO PDF A4 ---
def gerar_pdf_a4_cliente(dados):
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.add_page()
    logo_path = dados.get('LOGO_CLI_PATH')
    if logo_path and os.path.exists(logo_path):
        try:
            pdf.image(logo_path, x=75, y=10, w=60)
            pdf.ln(35)
        except: pdf.ln(10)
    else: pdf.ln(10)
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, f"{str(dados.get('CLIENTE', 'ORDEM DE SERVIÇO'))}", ln=True, align='C')
    pdf.ln(5); pdf.line(10, pdf.get_y(), 200, pdf.get_y()); pdf.ln(5)
    pdf.set_font("Arial", size=10)
    campos_excluir = ["VALOR_TOTAL", "LOGO_CLI_PATH", "ASS_PRESTADOR", "ASS_SOLICITANTE"]
    for chave, valor in dados.items():
        if chave not in campos_excluir:
            pdf.set_fill_color(245, 245, 245)
            pdf.cell(55, 7, txt=f"{chave}:", border=1, fill=True)
            pdf.cell(135, 7, txt=f"{str(valor)}", border=1); pdf.ln()
    pdf.ln(20)
    pdf.cell(95, 10, "__________________________", 0, 0, 'C')
    pdf.cell(95, 10, "__________________________", 0, 1, 'C')
    pdf.set_font("Arial", 'B', 9)
    pdf.cell(95, 5, f"{str(dados.get('ASS_PRESTADOR', 'PRESTADOR'))}", 0, 0, 'C')
    pdf.cell(95, 5, f"{str(dados.get('ASS_SOLICITANTE', 'SOLICITANTE'))}", 0, 1, 'C')
    return pdf.output(dest='S').encode('latin-1', 'ignore')

# --- NAVEGAÇÃO LATERAL (LOGO NAVEGÁVEL) ---
with st.sidebar:
    if os.path.exists("LOGO.PNG"):
        # A logo agora é um botão de imagem que reseta para o Menu de Ícones
        if st.button("🏠 RETORNAR AO PAINEL", use_container_width=True):
            st.session_state.tela = "MENU_ICONES"
            st.rerun()
        st.image("LOGO.PNG", use_container_width=True)
    st.divider()
    if st.button("📊 RESUMO FINANCEIRO", use_container_width=True):
        st.session_state.tela = "FINANCEIRO"
        st.rerun()

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
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("⏳ AGENDAMENTO", use_container_width=True): st.session_state.tela = "AGENDAMENTO"; st.rerun()
    with c2:
        if st.button("💰 FINANCEIRO", use_container_width=True): st.session_state.tela = "FINANCEIRO"; st.rerun()
    with c3:
        if st.button("📝 NOVO CADASTRO", use_container_width=True): st.session_state.tela = "CADASTRO"; st.rerun()

elif st.session_state.tela == "CADASTRO":
    st.title("📝 Cadastro de Missão")
    with st.form("f_cadastro"):
        col_c1, col_c2 = st.columns([2, 1])
        cli_n = col_c1.text_input("CLIENTE")
        logo_c = col_c2.file_uploader("LOGO CLIENTE", type=['png', 'jpg'])
        c1, c2 = st.columns(2)
        with c1:
            os_n = st.text_input("O.S Nº")
            d1 = st.date_input("INÍCIO")
            loc_o = st.text_input("ORIGEM")
            tipo = st.selectbox("TIPO", ["ESCOLTA", "POSTO"])
        with c2:
            emp = st.text_input("EMPURRADOR")
            d2 = st.date_input("FIM")
            sai_d = st.text_input("DESTINO")
            stt = st.selectbox("STATUS", ["ANDAMENTO", "ENCERRADO"])
        
        desc = st.text_area("DESCRIÇÃO DO SERVIÇO")
        
        ca1, ca2 = st.columns(2)
        as_p = ca1.text_input("ASS. PRESTADOR")
        as_s = ca2.text_input("ASS. SOLICITANTE")

        if st.form_submit_button("✅ SALVAR"):
            path = f"logo_{os_n}.png" if logo_c else None
            if logo_c:
                with open(path, "wb") as f: f.write(logo_c.getbuffer())
            dias = (d2 - d1).days if (d2 - d1).days > 0 else 1
            st.session_state.db_os.append({
                "CLIENTE": cli_n, "O.S": os_n, "INÍCIO": d1.strftime('%d/%m/%Y'),
                "FIM": d2.strftime('%d/%m/%Y'), "ORIGEM": loc_o, "DESTINO": sai_d,
                "EMPURRADOR": emp, "DESCRIÇÃO DO SERVIÇO": desc, "STATUS": stt,
                "VALOR_TOTAL": dias * (1870.0 if tipo == "ESCOLTA" else 970.0),
                "ASS_PRESTADOR": as_p, "ASS_SOLICITANTE": as_s, "LOGO_CLI_PATH": path
            })
            st.session_state.tela = "AGENDAMENTO"; st.rerun()

elif st.session_state.tela == "AGENDAMENTO":
    st.title("⏳ Agendamento")
    if st.session_state.db_os:
        df = pd.DataFrame(st.session_state.db_os)
        st.dataframe(df[["CLIENTE", "O.S", "INÍCIO", "STATUS"]], use_container_width=True)
        for i, row in df.iterrows():
            with st.expander(f"O.S {row['O.S']}"):
                if st.button(f"🟠 EDITAR/FINALIZAR", key=f"ed_{i}"):
                    st.session_state.editando_idx = i; st.session_state.tela = "EDITAR"; st.rerun()
                pdf = gerar_pdf_a4_cliente(row.to_dict())
                st.download_button("📥 BAIXAR PDF", data=pdf, file_name=f"OS_{row['O.S']}.pdf", key=f"dl_{i}")
    else: st.info("Sem registros.")

elif st.session_state.tela == "FINANCEIRO":
    st.title("💰 Financeiro")
    if st.session_state.db_os:
        df_f = pd.DataFrame(st.session_state.db_os)
        st.dataframe(df_f, use_container_width=True)
