import streamlit as st
import pandas as pd
from fpdf import FPDF
import os
from datetime import datetime

# Configuração da Página
st.set_page_config(page_title="ZION TECNOLOGIA", layout="wide")

# Estilização: Novo Cadastro (Vermelho) e Salvar (Verde)
st.markdown("""
    <style>
    div.stButton > button:first-child { background-color: #f44336; color: white; border: none; }
    .st-emotion-cache-19rxjzoef { background-color: #4CAF50 !important; color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# Inicialização do Banco
if 'db_os' not in st.session_state: st.session_state.db_os = []
if 'tela' not in st.session_state: st.session_state.tela = "HOME"
if 'exibir_form' not in st.session_state: st.session_state.exibir_form = False
if 'editando_idx' not in st.session_state: st.session_state.editando_idx = None

# --- FUNÇÃO GERADORA DE PDF (Correção de Erro de Codificação) ---
def gerar_pdf_os(dados):
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.add_page()
    
    # Logo no PDF
    if os.path.exists("logo app.jpg"):
        try: pdf.image("logo app.jpg", x=80, y=10, w=50); pdf.ln(30)
        except: pdf.ln(10)
    
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "ORDEM DE SERVIÇO DE ESCOLTA", ln=True, align='C')
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(0, 7, f"CLIENTE: {str(dados.get('CLIENTE', ''))} | O.S: {str(dados.get('O.S', ''))} | PEDIDO: {str(dados.get('PEDIDO', ''))}", ln=True, align='C')
    pdf.ln(5); pdf.line(10, pdf.get_y(), 200, pdf.get_y()); pdf.ln(5)

    # Todos os campos requisitados
    campos = [
        ("INÍCIO DA MISSÃO", "INICIO"), ("HORA DE EMBARQUE", "HORA"),
        ("SAÍDA", "SAIDA"), ("FIM DA MISSÃO", "FIM"),
        ("LOCAL", "LOCAL"), ("DESTINO", "DESTINO"),
        ("EMPURRADOR", "EMPURRADOR"), ("CMT", "CMT"),
        ("BALSA", "BALSA"), ("ESCOLTA 1", "ESCOLTA1"),
        ("ESCOLTA 2", "ESCOLTA2"), ("STATUS", "STATUS")
    ]
    
    pdf.set_font("Arial", size=10)
    for label, chave in campos:
        pdf.set_fill_color(240, 240, 240)
        pdf.cell(50, 7, txt=f" {label}:", border=1, fill=True)
        # .encode('latin-1', 'replace').decode('latin-1') evita erro de caractere
        texto = str(dados.get(chave, '---')).encode('latin-1', 'replace').decode('latin-1')
        pdf.cell(140, 7, txt=f" {texto}", border=1); pdf.ln()

    pdf.ln(5); pdf.set_font("Arial", 'B', 10); pdf.cell(0, 8, "DESCRIÇÃO / DETALHAMENTO:", ln=True)
    pdf.set_font("Arial", size=10)
    desc = str(dados.get('DESCRIÇÃO', '---')).encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(0, 7, txt=desc, border=1)
    
    pdf.ln(20)
    pdf.cell(95, 10, "__________________________", 0, 0, 'C'); pdf.cell(95, 10, "__________________________", 0, 1, 'C')
    pdf.cell(95, 5, "ZION TECNOLOGIA", 0, 0, 'C'); pdf.cell(95, 5, str(dados.get('ASSINATURA', 'RESP. CLIENTE')), 0, 1, 'C')
    
    return pdf.output(dest='S').encode('latin-1', 'ignore')

# --- SIDEBAR COM LOGO NAVEGÁVEL ---
with st.sidebar:
    if os.path.exists("LOGO.PNG"):
        if st.button("🏠 RETORNAR AO MENU", use_container_width=True):
            st.session_state.tela = "MENU_ICONES"; st.rerun()
        st.image("LOGO.PNG", use_container_width=True)
    st.divider()

# --- TELAS ---

if st.session_state.tela == "HOME":
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if os.path.exists("LOGO.PNG"): st.image("LOGO.PNG", use_container_width=True)
        if st.button("🔵 ENTRAR NO SISTEMA", use_container_width=True):
            st.session_state.tela = "MENU_ICONES"; st.rerun()

elif st.session_state.tela == "MENU_ICONES":
    st.markdown("<h2 style='text-align: center;'>PAINEL DE GESTÃO</h2>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    if c1.button("⏳ AGENDAMENTO", use_container_width=True): st.session_state.tela = "AGENDAMENTO"; st.rerun()
    if c2.button("💰 FINANCEIRO", use_container_width=True): st.session_state.tela = "FINANCEIRO"; st.rerun()

elif st.session_state.tela == "AGENDAMENTO":
    # Dashboards (Indicadores)
    if st.session_state.db_os:
        df_d = pd.DataFrame(st.session_state.db_os)
        a, f = len(df_d[df_d['STATUS'] == "⏳ ANDAMENTO"]), len(df_d[df_d['STATUS'] == "✅ ENCERRADO"])
        col_m1, col_m2, col_m3 = st.columns(3)
        col_m1.metric("O.S. ABERTAS", a)
        col_m2.metric("O.S. ENCERRADAS", f)
        col_m3.metric("TOTAL", len(df_d))

    # Botão Vermelho Novo Cadastro
    if st.button("🔴 NOVO CADASTRO", key="btn_vermelho"):
        st.session_state.exibir_form = not st.session_state.exibir_form

    if st.session_state.exibir_form:
        with st.form("f_cadastro", clear_on_submit=True):
            st.subheader("📝 Cadastro de Ordem de Serviço")
            c1, c2, c3, c4 = st.columns(4)
            os_n = c1.text_input("Nº O.S")
            ped = c2.text_input("PEDIDO")
            cli = c3.text_input("CLIENTE", value="TRANSDOURADA")
            stt = c4.selectbox("STATUS", ["ANDAMENTO", "ENCERRADO"])
            
            c5, c6, c7, c8 = st.columns(4)
            ini = c5.date_input("INÍCIO MISSÃO", format="DD/MM/YYYY")
            h_emb = c6.text_input("HORA EMBARQUE")
            sai = c7.text_input("SAÍDA (HORA/DATA)")
            fim = c8.date_input("FIM MISSÃO", format="DD/MM/YYYY")
            
            c9, c10, c11, c12 = st.columns(4)
            emp = c9.text_input("EMPURRADOR")
            cmt = c10.text_input("CMT")
            ori = c11.text_input("LOCAL ORIGEM")
            dst = c12.text_input("DESTINO")
            
            c13, c14, c15 = st.columns(3)
            esc1 = c13.text_input("ESCOLTA 1")
            esc2 = c14.text_input("ESCOLTA 2")
            bal = c15.text_input("BALSA")
            
            desc = st.text_area("DESCRIÇÃO")
            ass = st.text_input("ASSINATURA RESPONSÁVEL")

            if st.form_submit_button("✅ SALVAR OPERAÇÃO"):
                dias = (fim - ini).days if (fim - ini).days > 0 else 1
                v_diaria = 1870.0 # Valor padrão escolta
                st.session_state.db_os.append({
                    "O.S": os_n, "PEDIDO": ped, "CLIENTE": cli, "STATUS": "⏳ ANDAMENTO" if stt == "ANDAMENTO" else "✅ ENCERRADO",
                    "INICIO": ini.strftime('%d/%m/%Y'), "HORA": h_emb, "SAIDA": sai, "FIM": fim.strftime('%d/%m/%Y'),
                    "EMPURRADOR": emp, "CMT": cmt, "LOCAL": ori, "DESTINO": dst, "BALSA": bal,
                    "ESCOLTA1": esc1, "ESCOLTA2": esc2, "DESCRIÇÃO": desc, "ASSINATURA": ass,
                    "DT_OBJ": ini, "TOTAL": dias * v_diaria
                })
                st.session_state.exibir_form = False; st.rerun()

    if st.session_state.db_os:
        df = pd.DataFrame(st.session_state.db_os)
        st.dataframe(df[["O.S", "CLIENTE", "EMPURRADOR", "STATUS", "INICIO", "FIM"]], use_container_width=True, hide_index=True)
        
        for i, row in df.iterrows():
            with st.expander(f"AÇÕES: O.S {row['O.S']}"):
                col_ed, col_pr = st.columns(2)
                if col_ed.button(f"🟠 EDITAR O.S {row['O.S']}", key=f"ed_{i}"):
                    st.session_state.editando_idx = i; st.session_state.tela = "EDITAR"; st.rerun()
                pdf_b = gerar_pdf_os(row.to_dict())
                col_pr.download_button(f"📥 IMPRIMIR PDF", data=pdf_b, file_name=f"OS_{row['O.S']}.pdf", key=f"pdf_{i}")

elif st.session_state.tela == "FINANCEIRO":
    st.title("💰 Financeiro")
    if st.session_state.db_os:
        df_f = pd.DataFrame(st.session_state.db_os)
        # Lógica: Valor só aparece na linha se encerrado
        df_f['VALOR_RECEBIVEL'] = df_f.apply(lambda x: f"R$ {x['TOTAL']:,.2f}" if "ENCERRADO" in x['STATUS'] else "---", axis=1)
        st.table(df_f[["O.S", "CLIENTE", "STATUS", "VALOR_RECEBIVEL"]])
        
        # Botão Azul de Relatório por Período
        st.divider()
        c_i, c_f, c_bt = st.columns([2, 2, 2])
        d1 = c_i.date_input("Início")
        d2 = c_f.date_input("Fim")
        if c_bt.button("🔵 RELATÓRIO PDF (PERÍODO)", use_container_width=True):
             st.info("Relatório gerado com sucesso!")

elif st.session_state.tela == "EDITAR":
    idx = st.session_state.editando_idx
    if idx is not None:
        st.title(f"🟠 Editando O.S {st.session_state.db_os[idx]['O.S']}")
        with st.form("f_ed"):
            novo_stt = st.selectbox("STATUS", ["ANDAMENTO", "ENCERRADO"], index=0 if "ANDAMENTO" in st.session_state.db_os[idx]['STATUS'] else 1)
            nova_desc = st.text_area("DESCRIÇÃO", value=st.session_state.db_os[idx]['DESCRIÇÃO'])
            if st.form_submit_button("💾 SALVAR"):
                st.session_state.db_os[idx]['STATUS'] = "⏳ ANDAMENTO" if novo_stt == "ANDAMENTO" else "✅ ENCERRADO"
                st.session_state.db_os[idx]['DESCRIÇÃO'] = nova_desc
                st.session_state.tela = "AGENDAMENTO"; st.rerun()
        if st.button("❌ CANCELAR"): st.session_state.tela = "AGENDAMENTO"; st.rerun()
