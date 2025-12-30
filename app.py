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

# --- FUNÇÃO GERADORA DE PDF A4 (FOCO NO CLIENTE) ---
def gerar_pdf_a4_cliente(dados, logo_cliente_path=None):
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.add_page()
    
    # Tenta inserir a logo do cliente centralizada
    if logo_cliente_path and os.path.exists(logo_cliente_path):
        try:
            pdf.image(logo_cliente_path, x=75, y=10, w=60)
            pdf.ln(35)
        except:
            pdf.ln(10)
    else:
        pdf.ln(10)

    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, f"{str(dados.get('CLIENTE', 'ORDEM DE SERVIÇO'))}", ln=True, align='C')
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, f"ORDEM DE SERVIÇO Nº: {str(dados.get('O.S', '---'))}", ln=True, align='C')
    pdf.ln(5); pdf.line(10, pdf.get_y(), 200, pdf.get_y()); pdf.ln(5)
    
    pdf.set_font("Arial", size=10)
    # Lista de campos para sair no PDF na ordem correta
    campos_pdf = [
        "CLIENTE", "PEDIDO", "O.S", "INÍCIO", "EMBARQUE", "BALSAS", 
        "CTEs", "EMPURRADOR", "CMT", "SAÍDA", "FIM", "TÉRMINO", 
        "DESCRIÇÃO DO SERVIÇO", "STATUS"
    ]
    
    for chave in campos_pdf:
        if chave in dados:
            pdf.set_fill_color(245, 245, 245)
            pdf.cell(55, 8, txt=f"{chave}:", border=1, fill=True)
            pdf.cell(135, 8, txt=f"{str(dados[chave])}", border=1)
            pdf.ln()

    pdf.ln(20)
    pdf.cell(95, 10, "__________________________", 0, 0, 'C')
    pdf.cell(95, 10, "__________________________", 0, 1, 'C')
    pdf.set_font("Arial", 'B', 9)
    pdf.cell(95, 5, "ZION TECNOLOGIA (EXECUTOR)", 0, 0, 'C')
    pdf.cell(95, 5, "ASSINATURA CLIENTE (VALIDAÇÃO)", 0, 1, 'C')
    
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
    with st.form("f_cadastro", clear_on_submit=True):
        col_c1, col_c2 = st.columns([2, 1])
        cli_n = col_c1.text_input("CLIENTE")
        logo_c = col_c2.file_uploader("LOGO CLIENTE", type=['png', 'jpg'])
        
        c1, c2 = st.columns(2)
        with c1:
            ped = st.text_input("PEDIDO")
            os_n = st.text_input("O.S Nº")
            d1 = st.date_input("INÍCIO", format="DD/MM/YYYY")
            h_e = st.text_input("HORA EMBARQUE")
            bal = st.text_input("BALSAS")
            ct_e = st.text_input("CTEs")
            tipo = st.selectbox("SERVIÇO", ["ESCOLTA", "POSTO DE VIGILÂNCIA"])
        with c2:
            emp = st.text_input("EMPURRADOR")
            cmt = st.text_input("CMT")
            sai = st.text_input("SAÍDA")
            d2 = st.date_input("FIM", format="DD/MM/YYYY")
            h_t = st.text_input("HORA TÉRMINO")
            stt = st.selectbox("STATUS", ["ANDAMENTO", "ENCERRADO"])
        
        desc = st.text_area("DESCRIÇÃO DO SERVIÇO")
        
        if st.form_submit_button("✅ SALVAR MISSÃO"):
            path = None
            if logo_c is not None:
                path = f"logo_temp_{os_n}.png"
                with open(path, "wb") as f:
                    f.write(logo_c.getbuffer())
            
            dias = (d2 - d1).days if (d2 - d1).days > 0 else 1
            valor = dias * (1870.0 if tipo == "ESCOLTA" else 970.0)
            
            nova_os = {
                "CLIENTE": cli_n, "PEDIDO": ped, "O.S": os_n, "INÍCIO": d1.strftime('%d/%m/%Y'),
                "EMBARQUE": h_e, "BALSAS": bal, "CTEs": ct_e, "EMPURRADOR": emp,
                "CMT": cmt, "SAÍDA": sai, "FIM": d2.strftime('%d/%m/%Y'), "TÉRMINO": h_t,
                "DESCRIÇÃO DO SERVIÇO": desc, "STATUS": stt, "VALOR_TOTAL": valor, "LOGO_CLI_PATH": path
            }
            st.session_state.db_os.append(nova_os)
            st.success("O.S Salva com sucesso!")
            st.session_state.tela = "AGENDAMENTO"
            st.rerun()

elif st.session_state.tela == "AGENDAMENTO":
    st.title("⏳ Agendamento")
    if st.session_state.db_os:
        df = pd.DataFrame(st.session_state.db_os)
        st.dataframe(df[["CLIENTE", "O.S", "INÍCIO", "EMPURRADOR", "STATUS"]], use_container_width=True)
        
        for i, row in df.iterrows():
            with st.expander(f"O.S {row['O.S']} - {row['CLIENTE']}"):
                col_ed, col_pd = st.columns(2)
                if col_ed.button(f"🟠 EDITAR/FINALIZAR", key=f"btn_ed_{i}"):
                    st.session_state.editando_idx = i
                    st.session_state.tela = "EDITAR"
                    st.rerun()
                
                try:
                    pdf_data = gerar_pdf_a4_cliente(row.to_dict(), row.get('LOGO_CLI_PATH'))
                    col_pd.download_button("📥 BAIXAR O.S CLIENTE", data=pdf_data, file_name=f"OS_{row['O.S']}.pdf", key=f"dl_{i}")
                except:
                    col_pd.error("Erro ao gerar PDF")
    else: st.info("Nenhuma O.S registrada.")

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
                e_bal = st.text_input("BALSAS", value=str(d["BALSAS"]))
                e_h_e = st.text_input("HORA EMBARQUE", value=str(d["EMBARQUE"]))
            with c2:
                e_stt = st.selectbox("STATUS", ["ANDAMENTO", "ENCERRADO"], index=0 if d["STATUS"]=="ANDAMENTO" else 1)
                e_h_t = st.text_input("HORA TÉRMINO", value=str(d["TÉRMINO"]))
                e_sai = st.text_input("SAÍDA", value=str(d["SAÍDA"]))
                e_cte = st.text_input("CTEs", value=str(d["CTEs"]))
            e_desc = st.text_area("DESCRIÇÃO DO SERVIÇO", value=str(d["DESCRIÇÃO DO SERVIÇO"]))
            
            if st.form_submit_button("💾 SALVAR ALTERAÇÕES"):
                st.session_state.db_os[idx].update({
                    "CLIENTE": e_cli, "PEDIDO": e_ped, "STATUS": e_stt, "BALSAS": e_bal,
                    "EMBARQUE": e_h_e, "TÉRMINO": e_h_t, "SAÍDA": e_sai, "CTEs": e_cte, 
                    "DESCRIÇÃO DO SERVIÇO": e_desc
                })
                st.session_state.editando_idx = None
                st.session_state.tela = "AGENDAMENTO"
                st.rerun()
        if st.button("CANCELAR"): 
            st.session_state.tela = "AGENDAMENTO"
            st.rerun()

elif st.session_state.tela == "FINANCEIRO":
    st.title("💰 Financeiro")
    if st.session_state.db_os:
        df_f = pd.DataFrame(st.session_state.db_os)
        df_encerrados = df_f[df_f['STATUS'] == "ENCERRADO"]
        if not df_encerrados.empty:
            st.metric("TOTAL RECEBÍVEL (ENCERRADOS)", f"R$ {df_encerrados['VALOR_TOTAL'].sum():,.2f}")
            st.table(df_encerrados[["O.S", "CLIENTE", "VALOR_TOTAL", "STATUS"]])
        else: st.warning("Nenhuma missão encerrada para faturamento.")
    else: st.info("Sem dados.")
