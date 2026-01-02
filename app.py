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

# --- FUNÇÃO GERADORA DE PDF (ESTRUTURA COMPLETA) ---
def gerar_pdf_zion(dados):
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.add_page()
    
    # Logo do Cliente (logo app.jpg)
    logo_cliente = "logo app.jpg"
    if os.path.exists(logo_cliente):
        try:
            pdf.image(logo_cliente, x=65, y=10, w=80)
            pdf.ln(30)
        except: pdf.ln(10)
    else: pdf.ln(10)

    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "ORDEM DE SERVIÇO DE ESCOLTA", ln=True, align='C')
    pdf.set_font("Arial", 'B', 11)
    # Campo CLIENTE adicionado no topo do PDF
    pdf.cell(0, 7, f"CLIENTE: {str(dados.get('CLIENTE', '---'))}", ln=True, align='C')
    pdf.cell(0, 7, f"O.S Nº: {str(dados.get('O.S', '---'))} | PEDIDO: {str(dados.get('PEDIDO', '---'))}", ln=True, align='C')
    pdf.ln(5); pdf.line(10, pdf.get_y(), 200, pdf.get_y()); pdf.ln(5)
    
    pdf.set_font("Arial", size=10)
    campos_pdf = [
        ("INÍCIO DA MISSÃO", "INICIO"), ("HORA EMBARQUE", "HORA"),
        ("FIM DA MISSÃO", "FIM"), ("LOCAL", "LOCAL"),
        ("EMPURRADOR", "EMPURRADOR"), ("CMT", "CMT"),
        ("SAÍDA", "SAIDA"), ("DESTINO", "DESTINO"),
        ("BALSAS", "BALSA"), ("ESCOLTA 1", "ESCOLTA1"),
        ("ESCOLTA 2", "ESCOLTA2"), ("STATUS ATUAL", "STATUS")
    ]
    
    for label, chave in campos_pdf:
        valor = dados.get(chave, "---")
        pdf.set_fill_color(245, 245, 245)
        pdf.set_font("Arial", 'B', 10)
        pdf.cell(50, 7, txt=f" {label}:", border=1, fill=True)
        pdf.set_font("Arial", size=10)
        pdf.cell(140, 7, txt=f" {str(valor)}", border=1); pdf.ln()

    # Detalhamento
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(0, 8, "DETALHAMENTO DA MISSÃO:", ln=True)
    pdf.set_font("Arial", size=10)
    pdf.multi_cell(0, 7, txt=str(dados.get('DESCRIÇÃO', '---')), border=1)

    # Assinaturas
    pdf.ln(25)
    pdf.cell(95, 10, "__________________________", 0, 0, 'C')
    pdf.cell(95, 10, "__________________________", 0, 1, 'C')
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(95, 5, "SOLICITANTE", 0, 0, 'C')
    pdf.cell(95, 5, "RESPONSÁVEL CLIENTE", 0, 1, 'C')
    
    return pdf.output(dest='S').encode('latin-1', 'ignore')

# --- SIDEBAR ---
with st.sidebar:
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
    if st.button("⬅️ VOLTAR"):
        st.session_state.tela = "MENU_ICONES"; st.rerun()
    
    st.title("⏳ Agendamento e Novo Cadastro")
    
    # FORMULÁRIO DE CADASTRO
    with st.expander("➕ NOVO CADASTRO", expanded=False):
        with st.form("f_cadastro", clear_on_submit=True):
            c1, c2, c3 = st.columns(3)
            with c1:
                cli = st.text_input("NOME DO CLIENTE", value="TRANSDOURADA") # CAMPO ADICIONADO
                ped = st.text_input("PEDIDO")
                os_n = st.text_input("O.S")
                ini = st.date_input("INÍCIO DA MISSÃO")
                h_emb = st.text_input("HORA DE EMBARQUE")
            with c2:
                emp = st.text_input("EMPURRADOR")
                cmt = st.text_input("CMT")
                ori = st.text_input("LOCAL")
                sai = st.text_input("SAÍDA")
                fim_m = st.date_input("FIM DA MISSÃO")
            with c3:
                esc1 = st.text_input("ESCOLTA 1")
                esc2 = st.text_input("ESCOLTA 2")
                dest = st.text_input("DESTINO")
                stt = st.selectbox("STATUS", ["ANDAMENTO", "ENCERRADO"])
            
            bal = st.text_area("BALSA")
            desc = st.text_area("DESCRIÇÃO")
            ass_nome = st.text_input("ASSINATURA (NOME)")

            if st.form_submit_button("✅ SALVAR"):
                st.session_state.db_os.append({
                    "O.S": os_n, "INICIO": ini.strftime('%d/%m/%Y'), "HORA": h_emb,
                    "LOCAL": ori, "EMPURRADOR": emp, "CMT": cmt, "SAIDA": sai,
                    "FIM": fim_m.strftime('%d/%m/%Y'), "ESCOLTA1": esc1, "ESCOLTA2": esc2,
                    "DESCRIÇÃO": desc, "ASSINATURA": ass_nome, "CLIENTE": cli,
                    "BALSA": bal, "DESTINO": dest, "PEDIDO": ped, "STATUS": stt
                })
                st.success("Cadastro realizado!")
                st.rerun()

    st.divider()
    
    # TABELA DE AGENDAMENTOS
    if st.session_state.db_os:
        df = pd.DataFrame(st.session_state.db_os)
        colunas_ordem = [
            "O.S", "INICIO", "HORA", "LOCAL", "EMPURRADOR", "CMT", "SAIDA", 
            "FIM", "ESCOLTA1", "ESCOLTA2", "DESCRIÇÃO", "ASSINATURA", 
            "CLIENTE", "BALSA", "DESTINO", "PEDIDO"
        ]
        st.write("### Registros de Missões")
        st.dataframe(df[colunas_ordem], use_container_width=True)
        
        for i, row in df.iterrows():
            with st.expander(f"⚙️ Ações O.S {row['O.S']} - {row['CLIENTE']}"):
                col_btn1, col_btn2 = st.columns(2)
                if col_btn1.button(f"🟠 EDITAR O.S {row['O.S']}", key=f"ed_{i}"):
                    st.session_state.editando_idx = i
                    st.session_state.tela = "EDITAR"
                    st.rerun()
                
                pdf_b = gerar_pdf_zion(row.to_dict())
                col_btn2.download_button(f"📥 BAIXAR PDF O.S {row['O.S']}", data=pdf_b, 
                                       file_name=f"OS_{row['O.S']}.pdf", key=f"pdf_{i}")

elif st.session_state.tela == "EDITAR":
    idx = st.session_state.editando_idx
    if idx is not None:
        st.title(f"🟠 Editando O.S {st.session_state.db_os[idx]['O.S']}")
        with st.form("f_editar"):
            # Campos para edição (Exemplos)
            ed_cli = st.text_input("CLIENTE", value=st.session_state.db_os[idx]['CLIENTE'])
            ed_stt = st.selectbox("STATUS", ["ANDAMENTO", "ENCERRADO"], 
                                    index=0 if st.session_state.db_os[idx]['STATUS'] == "ANDAMENTO" else 1)
            ed_desc = st.text_area("DESCRIÇÃO", value=st.session_state.db_os[idx]['DESCRIÇÃO'])
            
            if st.form_submit_button("💾 SALVAR ALTERAÇÕES"):
                st.session_state.db_os[idx]['CLIENTE'] = ed_cli
                st.session_state.db_os[idx]['STATUS'] = ed_stt
                st.session_state.db_os[idx]['DESCRIÇÃO'] = ed_desc
                st.session_state.tela = "AGENDAMENTO"
                st.rerun()
        if st.button("❌ CANCELAR"):
            st.session_state.tela = "AGENDAMENTO"
            st.rerun()

elif st.session_state.tela == "FINANCEIRO":
    if st.button("⬅️ VOLTAR"):
        st.session_state.tela = "MENU_ICONES"; st.rerun()
    st.title("💰 Financeiro")
    if st.session_state.db_os:
        st.dataframe(pd.DataFrame(st.session_state.db_os), use_container_width=True)
