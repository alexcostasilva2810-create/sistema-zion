import streamlit as st
import pandas as pd
from fpdf import FPDF
import os
import base64

# Configuração da Página
st.set_page_config(page_title="ZION TECNOLOGIA", layout="wide")

# Inicialização do Banco de Dados
if 'db_os' not in st.session_state: st.session_state.db_os = []
if 'lista_emp' not in st.session_state: st.session_state.lista_emp = []
if 'tela' not in st.session_state: st.session_state.tela = "HOME"

# --- FUNÇÃO PDF A4 PROFISSIONAL ---
def gerar_pdf_a4_cliente(dados):
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.add_page()
    
    # Recupera a logo do cliente se houver
    logo_path = dados.get('LOGO_CLI_PATH')
    if logo_path and os.path.exists(logo_path):
        try:
            pdf.image(logo_path, x=75, y=10, w=60)
            pdf.ln(35)
        except: pdf.ln(10)
    else: pdf.ln(10)

    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, f"{str(dados.get('CLIENTE', 'ORDEM DE SERVIÇO'))}", ln=True, align='C')
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, f"O.S Nº: {str(dados.get('O.S', '---'))} | PEDIDO: {str(dados.get('PEDIDO', '---'))}", ln=True, align='C')
    pdf.ln(5); pdf.line(10, pdf.get_y(), 200, pdf.get_y()); pdf.ln(5)
    
    pdf.set_font("Arial", size=10)
    # Exibe campos operacionais no PDF
    excluir = ["VALOR_TOTAL", "LOGO_CLI_PATH", "ASSINATURA_PRESTADOR", "ASSINATURA_SOLICITANTE"]
    for chave, valor in dados.items():
        if chave not in excluir:
            pdf.set_fill_color(245, 245, 245)
            pdf.cell(55, 7, txt=f"{chave}:", border=1, fill=True)
            pdf.cell(135, 7, txt=f"{str(valor)}", border=1); pdf.ln()

    # --- CAMPOS DE ASSINATURA VIRTUAL E FÍSICA ---
    pdf.ln(20)
    # Linhas
    pdf.cell(95, 10, "__________________________", 0, 0, 'C')
    pdf.cell(95, 10, "__________________________", 0, 1, 'C')
    
    # Nomes da Assinatura Virtual (Digitados no sistema)
    pdf.set_font("Arial", 'B', 9)
    pdf.cell(95, 5, f"{str(dados.get('ASSINATURA_PRESTADOR', 'ASSINATURA DO PRESTADOR'))}", 0, 0, 'C')
    pdf.cell(95, 5, f"{str(dados.get('ASSINATURA_SOLICITANTE', 'ASSINATURA DO SOLICITANTE'))}", 0, 1, 'C')
    
    pdf.set_font("Arial", 'I', 7)
    pdf.cell(95, 5, "(ZION TECNOLOGIA)", 0, 0, 'C')
    pdf.cell(95, 5, "(SOLICITANTE / CLIENTE)", 0, 1, 'C')

    return pdf.output(dest='S').encode('latin-1', 'ignore')

# --- NAVEGAÇÃO ---
with st.sidebar:
    if os.path.exists("LOGO.PNG"): st.image("LOGO.PNG")
    if st.button("🏠 MENU PRINCIPAL", use_container_width=True): 
        st.session_state.tela = "MENU_ICONES"; st.rerun()

# --- TELAS ---
if st.session_state.tela == "HOME":
    st.markdown("<h1 style='text-align: center;'>ZION TECNOLOGIA</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if os.path.exists("LOGO.PNG"): st.image("LOGO.PNG")
        if st.button("🔵 ENTRAR NO SISTEMA", use_container_width=True):
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
    st.title("📝 Novo Cadastro de Missão")
    with st.form("f_cadastro"):
        col_c1, col_c2 = st.columns([2, 1])
        cli_n = col_c1.text_input("CLIENTE (NOME)")
        logo_c = col_c2.file_uploader("SUBIR LOGO DO CLIENTE", type=['png', 'jpg'])
        
        c1, c2 = st.columns(2)
        with c1:
            ped = st.text_input("PEDIDO")
            os_n = st.text_input("O.S Nº")
            d1 = st.date_input("INÍCIO DA MISSÃO", format="DD/MM/YYYY")
            h_e = st.text_input("HORA EMBARQUE")
            loc_origem = st.text_input("LOCAL (ORIGEM)")
            bal = st.text_input("BALSAS")
            tipo = st.selectbox("SERVIÇO", ["ESCOLTA", "POSTO DE VIGILÂNCIA"])
        with c2:
            emp = st.text_input("EMPURRADOR")
            cmt = st.text_input("CMT")
            sai = st.text_input("SAÍDA (DESTINO)")
            d2 = st.date_input("FIM DA MISSÃO", format="DD/MM/YYYY")
            h_t = st.text_input("HORA TÉRMINO")
            despesas = st.number_input("DESPESAS (R$)", min_value=0.0)
            stt = st.selectbox("STATUS", ["ANDAMENTO", "ENCERRADO"])
        
        desc = st.text_area("DESCRIÇÃO DO SERVIÇO")
        
        st.subheader("🖋️ Validação e Assinaturas Virtuais")
        col_as1, col_as2 = st.columns(2)
        ass_prest = col_as1.text_input("NOME DO PRESTADOR (ASS. VIRTUAL)")
        ass_solic = col_as2.text_input("NOME DO SOLICITANTE (ASS. VIRTUAL)")

        if st.form_submit_button("✅ SALVAR MISSÃO"):
            # Salva logo em pasta local para garantir que o PDF a encontre
            path = None
            if logo_c:
                path = f"logo_os_{os_n}.png"
                with open(path, "wb") as f: f.write(logo_c.getbuffer())
            
            dias = (d2 - d1).days if (d2 - d1).days > 0 else 1
            st.session_state.db_os.append({
                "CLIENTE": cli_n, "PEDIDO": ped, "O.S": os_n, "INÍCIO": d1.strftime('%d/%m/%Y'),
                "EMBARQUE": h_e, "LOCAL ORIGEM": loc_origem, "SAÍDA DESTINO": sai, "BALSAS": bal, 
                "EMPURRADOR": emp, "CMT": cmt, "FIM": d2.strftime('%d/%m/%Y'), "TÉRMINO": h_t,
                "DIAS": dias, "DESCRIÇÃO DO SERVIÇO": desc, "STATUS": stt, 
                "ASSINATURA_PRESTADOR": ass_prest, "ASSINATURA_SOLICITANTE": ass_solic,
                "VALOR_TOTAL": dias * (1870.0 if tipo == "ESCOLTA" else 970.0), "DESPESAS": despesas, "LOGO_CLI_PATH": path
            })
            st.session_state.tela = "AGENDAMENTO"; st.rerun()

elif st.session_state.tela == "AGENDAMENTO":
    st.title("⏳ Agendamento")
    if st.session_state.db_os:
        df = pd.DataFrame(st.session_state.db_os)
        st.dataframe(df[["CLIENTE", "O.S", "PEDIDO", "EMPURRADOR", "STATUS"]], use_container_width=True)
        for i, row in df.iterrows():
            with st.expander(f"Ações: O.S {row['O.S']} - {row['CLIENTE']}"):
                col_ed, col_pd = st.columns(2)
                if col_ed.button(f"🟠 EDITAR/FINALIZAR", key=f"btn_ed_{i}"):
                    st.session_state.editando_idx = i; st.session_state.tela = "EDITAR"; st.rerun()
                
                pdf_bytes = gerar_pdf_a4_cliente(row.to_dict())
                col_pd.download_button("📥 BAIXAR O.S EM A4", data=pdf_bytes, file_name=f"OS_{row['O.S']}.pdf", key=f"dl_{i}")

elif st.session_state.tela == "FINANCEIRO":
    st.title("💰 Financeiro Completo")
    if st.session_state.db_os:
        df_f = pd.DataFrame(st.session_state.db_os)
        cols_fin = ["PEDIDO", "O.S", "CLIENTE", "INÍCIO", "FIM", "LOCAL ORIGEM", "SAÍDA DESTINO", "EMPURRADOR", "DIAS", "VALOR_TOTAL", "DESPESAS", "STATUS"]
        st.dataframe(df_f[cols_fin], use_container_width=True)
