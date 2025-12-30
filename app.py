import streamlit as st
import pandas as pd
from fpdf import FPDF
import os

# Configuração da Página
st.set_page_config(page_title="ZION TECNOLOGIA", layout="wide")

# Inicialização do Banco de Dados
if 'db_os' not in st.session_state: st.session_state.db_os = []
if 'lista_emp' not in st.session_state: st.session_state.lista_emp = []
if 'tela' not in st.session_state: st.session_state.tela = "HOME"
if 'editando_idx' not in st.session_state: st.session_state.editando_idx = None

# --- FUNÇÃO PDF A4 ---
def gerar_pdf_a4_cliente(dados, logo_cliente_path=None):
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.add_page()
    if logo_cliente_path and os.path.exists(logo_cliente_path):
        try:
            pdf.image(logo_cliente_path, x=75, y=10, w=60)
            pdf.ln(35)
        except: pdf.ln(10)
    else: pdf.ln(10)
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, f"{str(dados.get('CLIENTE', 'ORDEM DE SERVIÇO'))}", ln=True, align='C')
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, f"ORDEM DE SERVIÇO Nº: {str(dados.get('O.S', '---'))}", ln=True, align='C')
    pdf.ln(5); pdf.line(10, pdf.get_y(), 200, pdf.get_y()); pdf.ln(5)
    pdf.set_font("Arial", size=10)
    for chave, valor in dados.items():
        if chave not in ["VALOR_TOTAL", "LOGO_CLI_PATH", "DESPESAS"]:
            pdf.set_fill_color(245, 245, 245)
            pdf.cell(55, 8, txt=f"{chave}:", border=1, fill=True)
            pdf.cell(135, 8, txt=f"{str(valor)}", border=1); pdf.ln()
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
    st.title("📝 Novo Cadastro")
    with st.form("f_cadastro"):
        col_c1, col_c2 = st.columns([2, 1])
        cli_n = col_c1.text_input("CLIENTE")
        logo_c = col_c2.file_uploader("LOGO CLIENTE", type=['png', 'jpg'])
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
            despesas = st.number_input("DESPESAS (R$)", min_value=0.0, step=10.0)
            stt = st.selectbox("STATUS", ["ANDAMENTO", "ENCERRADO"])
        desc = st.text_area("DESCRIÇÃO DO SERVIÇO")
        
        if st.form_submit_button("✅ SALVAR MISSÃO"):
            path = f"logo_{os_n}.png" if logo_c else None
            if logo_c:
                with open(path, "wb") as f: f.write(logo_c.getbuffer())
            dias = (d2 - d1).days if (d2 - d1).days > 0 else 1
            valor_linha = dias * (1870.0 if tipo == "ESCOLTA" else 970.0)
            st.session_state.db_os.append({
                "CLIENTE": cli_n, "PEDIDO": ped, "O.S": os_n, "INÍCIO": d1.strftime('%d/%m/%Y'),
                "EMBARQUE": h_e, "LOCAL ORIGEM": loc_origem, "SAÍDA DESTINO": sai, "BALSAS": bal, 
                "EMPURRADOR": emp, "CMT": cmt, "FIM": d2.strftime('%d/%m/%Y'), "TÉRMINO": h_t,
                "DIAS": dias, "DESCRIÇÃO DO SERVIÇO": desc, "STATUS": stt, 
                "VALOR_TOTAL": valor_linha, "DESPESAS": despesas, "LOGO_CLI_PATH": path
            })
            st.session_state.tela = "AGENDAMENTO"; st.rerun()

elif st.session_state.tela == "AGENDAMENTO":
    st.title("⏳ Agendamento")
    if st.session_state.db_os:
        df = pd.DataFrame(st.session_state.db_os)
        st.dataframe(df[["CLIENTE", "O.S", "INÍCIO", "EMPURRADOR", "STATUS"]], use_container_width=True)
        for i, row in df.iterrows():
            with st.expander(f"Ações: O.S {row['O.S']} - {row['CLIENTE']}"):
                col_ed, col_pd = st.columns(2)
                if col_ed.button(f"🟠 EDITAR/FINALIZAR", key=f"btn_ed_{i}"):
                    st.session_state.editando_idx = i; st.session_state.tela = "EDITAR"; st.rerun()
                pdf = gerar_pdf_a4_cliente(row.to_dict(), row['LOGO_CLI_PATH'])
                col_pd.download_button("📥 PDF A4", data=pdf, file_name=f"OS_{row['O.S']}.pdf", key=f"btn_pdf_{i}")
    else: st.info("Vazio.")

elif st.session_state.tela == "EDITAR":
    idx = st.session_state.editando_idx
    if idx is not None:
        d = st.session_state.db_os[idx]
        st.title(f"🟠 Editar O.S {d['O.S']}")
        with st.form("f_edit"):
            c1, c2 = st.columns(2)
            with c1:
                e_cli = st.text_input("CLIENTE", value=str(d["CLIENTE"]))
                e_ped = st.text_input("PEDIDO", value=str(d["PEDIDO"]))
                e_orig = st.text_input("LOCAL ORIGEM", value=str(d["LOCAL ORIGEM"]))
                e_desp = st.number_input("DESPESAS (R$)", value=float(d["DESPESAS"]))
            with c2:
                e_stt = st.selectbox("STATUS", ["ANDAMENTO", "ENCERRADO"], index=0 if d["STATUS"]=="ANDAMENTO" else 1)
                e_sai = st.text_input("SAÍDA DESTINO", value=str(d["SAÍDA DESTINO"]))
                e_h_t = st.text_input("HORA TÉRMINO", value=str(d["TÉRMINO"]))
            e_desc = st.text_area("DESCRIÇÃO DO SERVIÇO", value=str(d["DESCRIÇÃO DO SERVIÇO"]))
            if st.form_submit_button("💾 ATUALIZAR"):
                st.session_state.db_os[idx].update({
                    "CLIENTE": e_cli, "PEDIDO": e_ped, "STATUS": e_stt, "LOCAL ORIGEM": e_orig,
                    "SAÍDA DESTINO": e_sai, "TÉRMINO": e_h_t, "DESCRIÇÃO DO SERVIÇO": e_desc, "DESPESAS": e_desp
                })
                st.session_state.editando_idx = None; st.session_state.tela = "AGENDAMENTO"; st.rerun()

elif st.session_state.tela == "FINANCEIRO":
    st.title("💰 Financeiro e Fechamento")
    if st.session_state.db_os:
        df_f = pd.DataFrame(st.session_state.db_os)
        # Colunas Solicitadas para o Cruzamento
        cols_fin = ["PEDIDO", "O.S", "CLIENTE", "INÍCIO", "FIM", "LOCAL ORIGEM", "SAÍDA DESTINO", "EMPURRADOR", "DIAS", "VALOR_TOTAL", "DESPESAS", "STATUS"]
        
        # Filtro para ver apenas encerrados ou todos
        ver_todos = st.checkbox("Mostrar Missões em Andamento")
        if not ver_todos:
            df_exibir = df_f[df_f['STATUS'] == "ENCERRADO"]
        else:
            df_exibir = df_f

        st.metric("FATURAMENTO TOTAL (EXIBIDO)", f"R$ {df_exibir['VALOR_TOTAL'].sum():,.2f}")
        st.dataframe(df_exibir[cols_fin], use_container_width=True)

        st.divider()
        st.subheader("📁 Anexo de Notas Fiscais")
        for i, row in df_exibir.iterrows():
            with st.expander(f"Anexar NF para O.S {row['O.S']} - {row['CLIENTE']}"):
                st.file_uploader(f"Upload XML ou PDF da NF", key=f"nf_fin_{i}")
                if st.button("Confirmar Anexo", key=f"conf_nf_{i}"):
                    st.success(f"Nota Fiscal da O.S {row['O.S']} vinculada!")
    else: st.info("Sem dados para o financeiro.")
