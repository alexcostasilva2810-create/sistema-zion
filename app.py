import streamlit as st
import pandas as pd
from fpdf import FPDF
import os

# Configuração da Página
st.set_page_config(page_title="ZION TECNOLOGIA", layout="wide")

# Inicialização do Banco de Dados
if 'lista_empurradores' not in st.session_state:
    st.session_state.lista_empurradores = []
if 'db_os' not in st.session_state:
    st.session_state.db_os = []
if 'tela' not in st.session_state:
    st.session_state.tela = "HOME"
if 'editando_idx' not in st.session_state:
    st.session_state.editando_idx = None

# --- FUNÇÃO GERADORA DE PDF A4 ---
def gerar_pdf_a4(dados):
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.add_page()
    try:
        if os.path.exists("LOGO.PNG"):
            pdf.image("LOGO.PNG", x=10, y=8, w=35)
    except: pass
    pdf.set_font("Arial", 'B', 18)
    pdf.cell(0, 15, "ZION TECNOLOGIA", ln=True, align='C')
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "ORDEM DE SERVIÇO OFICIAL", ln=True, align='C')
    pdf.ln(10); pdf.line(10, 45, 200, 45); pdf.ln(5)
    pdf.set_font("Arial", size=10)
    for chave, valor in dados.items():
        if chave not in ["VALOR_TOTAL", "ID"]:
            pdf.set_fill_color(240, 240, 240)
            pdf.cell(55, 8, txt=f"{chave}:", border=1, fill=True)
            pdf.cell(135, 8, txt=f"{str(valor)}", border=1); pdf.ln()
    pdf.ln(25)
    pdf.cell(95, 10, "__________________________", 0, 0, 'C')
    pdf.cell(95, 10, "__________________________", 0, 1, 'C')
    pdf.set_font("Arial", 'B', 8)
    pdf.cell(95, 5, "ASSINATURA DO RESPONSÁVEL (ZION)", 0, 0, 'C')
    pdf.cell(95, 5, "ASSINATURA DO COLABORADOR (USUÁRIO)", 0, 1, 'C')
    return pdf.output(dest='S').encode('latin-1')

# --- NAVEGAÇÃO ---
with st.sidebar:
    if os.path.exists("LOGO.PNG"): st.image("LOGO.PNG", use_container_width=True)
    if st.button("🏠 MENU PRINCIPAL", use_container_width=True):
        st.session_state.tela = "MENU_ICONES"; st.rerun()

# --- TELAS ---
if st.session_state.tela == "HOME":
    st.markdown("<h1 style='text-align: center;'>ZION TECNOLOGIA</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if os.path.exists("LOGO.PNG"): st.image("LOGO.PNG", use_container_width=True)
        if st.button("🔵 ENTRAR NO SISTEMA", use_container_width=True):
            st.session_state.tela = "MENU_ICONES"; st.rerun()

elif st.session_state.tela == "MENU_ICONES":
    st.markdown("<h2 style='text-align: center;'>PAINEL DE GESTÃO</h2>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("⏳ AGENDAMENTO", use_container_width=True):
            st.session_state.tela = "AGENDAMENTO"; st.rerun()
    with c2:
        if st.button("💰 FINANCEIRO", use_container_width=True):
            st.session_state.tela = "FINANCEIRO"; st.rerun()
    with c3:
        if st.button("📝 NOVO CADASTRO", use_container_width=True):
            st.session_state.tela = "CADASTRO"; st.rerun()

elif st.session_state.tela == "CADASTRO":
    st.title("📝 Cadastro de Missão Completo")
    with st.expander("➕ CADASTRAR NOMES"):
        n = st.text_input("Nome do Empurrador:").upper()
        if st.button("SALVAR NOME"):
            st.session_state.lista_empurradores.append(n); st.rerun()
    
    with st.form("f_os"):
        c1, c2 = st.columns(2)
        with c1:
            ped = st.text_input("PEDIDO")
            os_n = st.text_input("NÚMERO DA O.S")
            d1 = st.date_input("INÍCIO DA MISSÃO", format="DD/MM/YYYY")
            h_emb = st.text_input("HORA DO EMBARQUE")
            loc = st.text_input("LOCAL")
            esc1 = st.text_input("ESCOLTA 1")
            tipo = st.selectbox("TIPO DE SERVIÇO", ["ESCOLTA", "POSTO DE VIGILÂNCIA"])
        with c2:
            emp = st.selectbox("EMPURRADOR", options=st.session_state.lista_empurradores)
            cmt = st.text_input("CMT")
            sai = st.text_input("SAÍDA")
            d2 = st.date_input("FIM DA MISSÃO", format="DD/MM/YYYY")
            h_term = st.text_input("HORA/TÉRMINO MISSÃO")
            esc2 = st.text_input("ESCOLTA 2")
            status = st.selectbox("STATUS", ["ANDAMENTO", "ENCERRADO"])
        
        if st.form_submit_button("✅ SALVAR E REGISTRAR"):
            dias = (d2 - d1).days if (d2 - d1).days > 0 else 1
            v_dia = 1870.0 if tipo == "ESCOLTA" else 970.0
            st.session_state.db_os.append({
                "PEDIDO": ped, "O.S": os_n, "INÍCIO": d1.strftime('%d/%m/%Y'),
                "EMBARQUE": h_emb, "LOCAL": loc, "ESCOLTA 1": esc1, "EMPURRADOR": emp,
                "CMT": cmt, "SAÍDA": sai, "FIM": d2.strftime('%d/%m/%Y'),
                "TÉRMINO": h_term, "ESCOLTA 2": esc2, "SERVIÇO": tipo,
                "STATUS": status, "VALOR_TOTAL": dias * v_dia
            })
            st.session_state.tela = "AGENDAMENTO"; st.rerun()

elif st.session_state.tela == "AGENDAMENTO":
    st.title("⏳ Agendamento e Programação")
    if st.session_state.db_os:
        df = pd.DataFrame(st.session_state.db_os)
        st.dataframe(df.drop(columns=["VALOR_TOTAL"]), use_container_width=True)
        
        for i, row in df.iterrows():
            with st.expander(f"Ações O.S {row['O.S']} - {row['EMPURRADOR']}"):
                col_edit, col_pdf = st.columns(2)
                # BOTÃO LARANJA PARA EDITAR
                if col_edit.button(f"🟠 EDITAR/FINALIZAR O.S {row['O.S']}", key=f"ed_{i}"):
                    st.session_state.editando_idx = i
                    st.session_state.tela = "EDITAR"
                    st.rerun()
                pdf_bytes = gerar_pdf_a4(row.to_dict())
                col_pdf.download_button(f"📥 BAIXAR O.S A4", data=pdf_bytes, file_name=f"OS_{row['O.S']}.pdf", key=f"pdf_{i}")
    else: st.info("Sem registros.")

elif st.session_state.tela == "EDITAR":
    idx = st.session_state.editando_idx
    if idx is not None:
        st.title(f"🟠 Editando O.S {st.session_state.db_os[idx]['O.S']}")
        with st.form("f_edicao"):
            # Carrega dados atuais
            d = st.session_state.db_os[idx]
            c1, c2 = st.columns(2)
            with c1:
                ped_e = st.text_input("PEDIDO", value=d["PEDIDO"])
                os_e = st.text_input("NÚMERO DA O.S", value=d["O.S"])
                loc_e = st.text_input("LOCAL", value=d["LOCAL"])
                h_emb_e = st.text_input("HORA EMBARQUE", value=d["EMBARQUE"])
            with c2:
                status_e = st.selectbox("STATUS", ["ANDAMENTO", "ENCERRADO"], index=0 if d["STATUS"]=="ANDAMENTO" else 1)
                h_term_e = st.text_input("HORA TÉRMINO", value=d["TÉRMINO"])
                sai_e = st.text_input("SAÍDA", value=d["SAÍDA"])
            
            if st.form_submit_button("💾 SALVAR ALTERAÇÕES"):
                st.session_state.db_os[idx].update({"PEDIDO": ped_e, "O.S": os_e, "LOCAL": loc_e, "STATUS": status_e, "EMBARQUE": h_emb_e, "TÉRMINO": h_term_e, "SAÍDA": sai_e})
                st.session_state.editando_idx = None
                st.session_state.tela = "AGENDAMENTO"
                st.success("Dados atualizados!")
                st.rerun()
        if st.button("CANCELAR"):
            st.session_state.tela = "AGENDAMENTO"; st.rerun()

elif st.session_state.tela == "FINANCEIRO":
    st.title("💰 Financeiro")
    if st.session_state.db_os:
        df_f = pd.DataFrame(st.session_state.db_os)
        st.metric("TOTAL FATURADO", f"R$ {df_f['VALOR_TOTAL'].sum():,.2f}")
        st.table(df_f[["O.S", "PEDIDO", "SERVIÇO", "VALOR_TOTAL", "STATUS"]])
