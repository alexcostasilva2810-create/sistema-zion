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

# --- FUNÇÃO GERADORA DE PDF A4 ---
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
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, f"O.S Nº: {str(dados.get('O.S', '---'))} | PEDIDO: {str(dados.get('PEDIDO', '---'))}", ln=True, align='C')
    pdf.ln(5); pdf.line(10, pdf.get_y(), 200, pdf.get_y()); pdf.ln(5)
    
    pdf.set_font("Arial", size=10)
    campos_exibir = [
        "INÍCIO", "FIM", "HORA EMBARQUE", "HORA TÉRMINO", "LOCAL (ORIGEM)", 
        "SAÍDA (DESTINO)", "EMPURRADOR", "CMT", "BALSAS", "CTEs", 
        "DESCRIÇÃO DO SERVIÇO", "STATUS"
    ]
    for chave in campos_exibir:
        valor = dados.get(chave, "---")
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

# --- NAVEGAÇÃO LATERAL (A LOGO É O BOTÃO) ---
with st.sidebar:
    if os.path.exists("LOGO.PNG"):
        if st.button("🔄 CLIQUE NA LOGO PARA VOLTAR", use_container_width=True):
            st.session_state.tela = "MENU_ICONES"
            st.rerun()
        # A imagem abaixo serve como o ícone visual do botão acima
        st.image("LOGO.PNG", use_container_width=True)
    st.divider()
    st.info("ZION TECNOLOGIA v2.0")

# --- TELAS ---
if st.session_state.tela == "HOME":
    st.markdown("<h1 style='text-align: center;'>ZION TECNOLOGIA</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if os.path.exists("LOGO.PNG"): st.image("LOGO.PNG")
        if st.button("🔵 INICIAR SISTEMA", use_container_width=True):
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
    if st.button("⬅️ RETORNAR AO PAINEL"):
        st.session_state.tela = "MENU_ICONES"; st.rerun()
    
    st.title("⏳ Agendamento e Novo Cadastro")
    
    # --- SEÇÃO DE CADASTRO UNIFICADA ---
    with st.expander("➕ CLIQUE PARA CADASTRAR NOVA MISSÃO", expanded=False):
        with st.form("f_cadastro_unificado"):
            col_c1, col_c2 = st.columns([2, 1])
            cli_n = col_c1.text_input("CLIENTE")
            logo_c = col_c2.file_uploader("LOGO CLIENTE", type=['png', 'jpg'])
            c1, c2 = st.columns(2)
            with c1:
                ped = st.text_input("PEDIDO")
                os_n = st.text_input("O.S Nº")
                d1 = st.date_input("INÍCIO DA MISSÃO")
                loc_o = st.text_input("LOCAL (ORIGEM)")
                bal = st.text_input("BALSAS")
                tipo = st.selectbox("SERVIÇO", ["ESCOLTA", "POSTO DE VIGILÂNCIA"])
            with c2:
                emp = st.text_input("EMPURRADOR")
                cmt = st.text_input("CMT")
                sai_d = st.text_input("SAÍDA (DESTINO)")
                d2 = st.date_input("FIM DA MISSÃO")
                h_t = st.text_input("HORA TÉRMINO")
                stt = st.selectbox("STATUS", ["ANDAMENTO", "ENCERRADO"])
            desc = st.text_area("DESCRIÇÃO DO SERVIÇO")
            as_p = st.text_input("NOME PRESTADOR (ASS. VIRTUAL)")
            as_s = st.text_input("NOME SOLICITANTE (ASS. VIRTUAL)")

            if st.form_submit_button("✅ SALVAR E REGISTRAR"):
                path = f"logo_{os_n}.png" if logo_c else None
                if logo_c:
                    with open(path, "wb") as f: f.write(logo_c.getbuffer())
                dias = (d2 - d1).days if (d2 - d1).days > 0 else 1
                st.session_state.db_os.append({
                    "CLIENTE": cli_n, "PEDIDO": ped, "O.S": os_n, "INÍCIO": d1.strftime('%d/%m/%Y'),
                    "FIM": d2.strftime('%d/%m/%Y'), "LOCAL (ORIGEM)": loc_o, "SAÍDA (DESTINO)": sai_d,
                    "BALSAS": bal, "EMPURRADOR": emp, "CMT": cmt, "DIAS": dias, "DESCRIÇÃO DO SERVIÇO": desc, 
                    "STATUS": stt, "VALOR_TOTAL": dias * (1870.0 if tipo == "ESCOLTA" else 970.0), 
                    "ASS_PRESTADOR": as_p, "ASS_SOLICITANTE": as_s, "LOGO_CLI_PATH": path
                })
                st.success("Missão cadastrada com sucesso!")
                st.rerun()

    st.divider()
    # --- LISTA DE AGENDAMENTOS ---
    if st.session_state.db_os:
        df = pd.DataFrame(st.session_state.db_os)
        st.dataframe(df[["CLIENTE", "O.S", "INÍCIO", "EMPURRADOR", "STATUS"]], use_container_width=True)
        for i, row in df.iterrows():
            with st.expander(f"Gerenciar O.S {row['O.S']} - {row['CLIENTE']}"):
                c_ed, c_pd = st.columns(2)
                if c_ed.button(f"🟠 EDITAR", key=f"e_{i}"):
                    st.session_state.editando_idx = i; st.session_state.tela = "EDITAR"; st.rerun()
                pdf_b = gerar_pdf_a4_cliente(row.to_dict())
                c_pd.download_button("📥 BAIXAR PDF A4", data=pdf_b, file_name=f"OS_{row['O.S']}.pdf", key=f"p_{i}")
    else: st.info("Nenhuma missão no banco de dados.")

elif st.session_state.tela == "EDITAR":
    if st.button("⬅️ CANCELAR E VOLTAR"):
        st.session_state.tela = "AGENDAMENTO"; st.rerun()
    # Lógica de edição permanece a mesma do código anterior...
    idx = st.session_state.editando_idx
    if idx is not None:
        d = st.session_state.db_os[idx]
        st.title(f"🟠 Editando O.S {d['O.S']}")
        with st.form("f_edit"):
            e_stt = st.selectbox("STATUS", ["ANDAMENTO", "ENCERRADO"], index=0 if d["STATUS"]=="ANDAMENTO" else 1)
            e_desc = st.text_area("DESCRIÇÃO", value=str(d["DESCRIÇÃO DO SERVIÇO"]))
            if st.form_submit_button("💾 SALVAR ALTERAÇÕES"):
                st.session_state.db_os[idx].update({"STATUS": e_stt, "DESCRIÇÃO DO SERVIÇO": e_desc})
                st.session_state.tela = "AGENDAMENTO"; st.rerun()

elif st.session_state.tela == "FINANCEIRO":
    if st.button("⬅️ RETORNAR AO PAINEL"):
        st.session_state.tela = "MENU_ICONES"; st.rerun()
    st.title("💰 Financeiro e Cruzamento de Dados")
    if st.session_state.db_os:
        df_f = pd.DataFrame(st.session_state.db_os)
        cols = ["PEDIDO", "O.S", "CLIENTE", "INÍCIO", "FIM", "LOCAL (ORIGEM)", "EMPURRADOR", "DIAS", "VALOR_TOTAL", "STATUS"]
        st.dataframe(df_f[cols], use_container_width=True)
        st.metric("FATURAMENTO TOTAL", f"R$ {df_f['VALOR_TOTAL'].sum():,.2f}")
    else: st.info("Sem dados financeiros.")
