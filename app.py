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

# --- FUNÇÃO GERADORA DE PDF A4 - FOCO NO CLIENTE ---
def gerar_pdf_a4_cliente(dados, logo_cliente_path=None):
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.add_page()
    
    # EVIDENCIAR APENAS O CLIENTE NO TOPO (CENTRALIZADO)
    if logo_cliente_path and os.path.exists(logo_cliente_path):
        # Tenta centralizar a logo do cliente (x=75 para uma logo de 60mm de largura)
        pdf.image(logo_cliente_path, x=75, y=10, w=60)
        pdf.ln(35) # Espaço maior após a logo para não sobrepor
    else:
        pdf.ln(10)

    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, f"{dados.get('CLIENTE', 'ORDEM DE SERVIÇO')}", ln=True, align='C')
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, f"ORDEM DE SERVIÇO Nº: {dados.get('O.S', '---')}", ln=True, align='C')
    
    pdf.ln(5); pdf.line(10, pdf.get_y(), 200, pdf.get_y()); pdf.ln(5)
    
    # Conteúdo da O.S
    pdf.set_font("Arial", size=10)
    for chave, valor in dados.items():
        # Não imprime campos técnicos ou financeiros no operacional
        if chave not in ["VALOR_TOTAL", "LOGO_CLI_PATH", "ID"]:
            pdf.set_fill_color(245, 245, 245)
            pdf.cell(55, 8, txt=f"{chave}:", border=1, fill=True)
            pdf.cell(135, 8, txt=f"{str(valor)}", border=1); pdf.ln()

    # ÁREA DE ASSINATURA
    pdf.ln(20)
    pdf.cell(95, 10, "__________________________", 0, 0, 'C')
    pdf.cell(95, 10, "__________________________", 0, 1, 'C')
    pdf.set_font("Arial", 'B', 9)
    pdf.cell(95, 5, "ZION TECNOLOGIA (EXECUTOR)", 0, 0, 'C')
    pdf.cell(95, 5, "ASSINATURA CLIENTE (VALIDAÇÃO)", 0, 1, 'C')

    return pdf.output(dest='S').encode('latin-1')

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
    st.title("📝 Cadastro de Missão")
    with st.form("f_completo"):
        col_cli1, col_cli2 = st.columns([2, 1])
        cliente_nome = col_cli1.text_input("CLIENTE (NOME)")
        logo_cli = col_cli2.file_uploader("SUBIR LOGO DO CLIENTE", type=['png', 'jpg'])
        
        c1, c2 = st.columns(2)
        with c1:
            ped = st.text_input("PEDIDO")
            os_n = st.text_input("NÚMERO DA O.S")
            d1 = st.date_input("INÍCIO DA MISSÃO", format="DD/MM/YYYY")
            h_emb = st.text_input("HORA EMBARQUE")
            balsas = st.text_input("BALSAS")
            ctes = st.text_input("CTEs")
            tipo = st.selectbox("SERVIÇO", ["ESCOLTA", "POSTO DE VIGILÂNCIA"])
        with c2:
            emp = st.selectbox("EMPURRADOR", options=st.session_state.lista_emp) if st.session_state.lista_emp else st.text_input("EMPURRADOR")
            cmt = st.text_input("CMT")
            sai = st.text_input("SAÍDA")
            d2 = st.date_input("FIM DA MISSÃO", format="DD/MM/YYYY")
            h_term = st.text_input("HORA TÉRMINO")
            status = st.selectbox("STATUS", ["ANDAMENTO", "ENCERRADO"])
        
        desc = st.text_area("DESCRIÇÃO DO SERVIÇO")
        
        if st.form_submit_button("✅ SALVAR MISSÃO"):
            path_cli = None
            if logo_cli:
                path_cli = f"logo_cli_{os_n}.png"
                with open(path_cli, "wb") as f:
                    f.write(logo_cli.getbuffer())

            dias = (d2 - d1).days if (d2 - d1).days > 0 else 1
            v_dia = 1870.0 if tipo == "ESCOLTA" else 970.0
            
            st.session_state.db_os.append({
                "CLIENTE": cliente_nome, "PEDIDO": ped, "O.S": os_n, "INÍCIO": d1.strftime('%d/%m/%Y'),
                "EMBARQUE": h_emb, "BALSAS": balsas, "CTEs": ctes, "EMPURRADOR": emp,
                "CMT": cmt, "SAÍDA": sai, "FIM": d2.strftime('%d/%m/%Y'), "TÉRMINO": h_term,
                "DESCRIÇÃO DO SERVIÇO": desc, "STATUS": status, "VALOR_TOTAL": dias * v_dia, "LOGO_CLI_PATH": path_cli
            })
            st.session_state.tela = "AGENDAMENTO"; st.rerun()

elif st.session_state.tela == "AGENDAMENTO":
    st.title("⏳ Agendamento")
    if st.session_state.db_os:
        df = pd.DataFrame(st.session_state.db_os)
        cols_v = ["CLIENTE", "O.S", "INÍCIO", "EMPURRADOR", "STATUS"]
        st.dataframe(df[cols_v], use_container_width=True)
        for i, row in df.iterrows():
            with st.expander(f"O.S {row['O.S']} - {row['CLIENTE']}"):
                col_a, col_b = st.columns(2)
                if col_a.button(f"🟠 EDITAR/FINALIZAR", key=f"ed_{i}"):
                    st.session_state.editando_idx = i; st.session_state.tela = "EDITAR"; st.rerun()
                pdf_b = gerar_pdf_a4_cliente(row.to_dict(), row['LOGO_CLI_PATH'])
                col_b.download_button("📥 BAIXAR O.S CLIENTE", data=pdf_b, file_name=f"OS_{row['CLIENTE']}.pdf", key=f"p_{i}")

elif st.session_state.tela == "FINANCEIRO":
    st.title("💰 Financeiro")
    if st.session_state.db_os:
        df_f = pd.DataFrame(st.session_state.db_os)
        df_encerrados = df_f[df_f['STATUS'] == "ENCERRADO"]
        if not df_encerrados.empty:
            st.metric("TOTAL RECEBÍVEL", f"R$ {df_encerrados['VALOR_TOTAL'].sum():,.2f}")
            st.table(df_encerrados[["O.S", "CLIENTE", "VALOR_TOTAL"]])
        else: st.warning("Nenhuma O.S encerrada.")
