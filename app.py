import streamlit as st
import pandas as pd
from fpdf import FPDF
import os
from datetime import datetime

# Configuração da Página
st.set_page_config(page_title="ZION TECNOLOGIA", layout="wide")

# Inicialização do Banco de Dados
if 'db_os' not in st.session_state: st.session_state.db_os = []
if 'tela' not in st.session_state: st.session_state.tela = "HOME"
if 'editando_idx' not in st.session_state: st.session_state.editando_idx = None

# --- FUNÇÃO GERADORA DE PDF O.S ---
def gerar_pdf_os(dados):
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.add_page()
    logo_cliente = "logo app.jpg"
    if os.path.exists(logo_cliente):
        try: pdf.image(logo_cliente, x=65, y=10, w=80); pdf.ln(30)
        except: pdf.ln(10)
    else: pdf.ln(10)

    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "ORDEM DE SERVIÇO DE ESCOLTA", ln=True, align='C')
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(0, 7, f"CLIENTE: {str(dados.get('CLIENTE', '---'))}", ln=True, align='C')
    pdf.cell(0, 7, f"O.S Nº: {str(dados.get('O.S', '---'))} | PEDIDO: {str(dados.get('PEDIDO', '---'))}", ln=True, align='C')
    pdf.ln(5); pdf.line(10, pdf.get_y(), 200, pdf.get_y()); pdf.ln(5)
    
    campos = [
        ("INÍCIO DA MISSÃO", "INICIO"), ("HORA EMBARQUE", "HORA"),
        ("FIM DA MISSÃO", "FIM"), ("LOCAL", "LOCAL"),
        ("EMPURRADOR", "EMPURRADOR"), ("CMT", "CMT"),
        ("BALSAS", "BALSA"), ("ESCOLTA 1", "ESCOLTA1"),
        ("ESCOLTA 2", "ESCOLTA2"), ("STATUS", "STATUS")
    ]
    
    pdf.set_font("Arial", size=10)
    for label, chave in campos:
        pdf.set_fill_color(245, 245, 245)
        pdf.cell(50, 7, txt=f" {label}:", border=1, fill=True)
        pdf.cell(140, 7, txt=f" {str(dados.get(chave, '---'))}", border=1); pdf.ln()

    pdf.ln(5); pdf.set_font("Arial", 'B', 10); pdf.cell(0, 8, "DETALHAMENTO DA MISSÃO:", ln=True)
    pdf.set_font("Arial", size=10); pdf.multi_cell(0, 7, txt=str(dados.get('DESCRIÇÃO', '---')), border=1)

    pdf.ln(25); pdf.cell(95, 10, "__________________________", 0, 0, 'C'); pdf.cell(95, 10, "__________________________", 0, 1, 'C')
    pdf.set_font("Arial", 'B', 10); pdf.cell(95, 5, "SOLICITANTE", 0, 0, 'C'); pdf.cell(95, 5, "RESPONSÁVEL CLIENTE", 0, 1, 'C')
    
    return pdf.output(dest='S').encode('latin-1', 'ignore')

# --- FUNÇÃO RELATÓRIO FINANCEIRO ---
def gerar_relatorio_financeiro(df_periodo, data_i, data_f):
    pdf = FPDF(orientation='L', unit='mm', format='A4')
    pdf.add_page()
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, f"RELATÓRIO FINANCEIRO: {data_i.strftime('%d/%m/%Y')} A {data_f.strftime('%d/%m/%Y')}", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 9)
    pdf.set_fill_color(220, 220, 220)
    pdf.cell(20, 8, "O.S", 1, 0, 'C', True); pdf.cell(60, 8, "CLIENTE", 1, 0, 'C', True)
    pdf.cell(30, 8, "INICIO", 1, 0, 'C', True); pdf.cell(30, 8, "FIM", 1, 0, 'C', True)
    pdf.cell(40, 8, "TIPO", 1, 0, 'C', True); pdf.cell(40, 8, "VALOR TOTAL", 1, 1, 'C', True)
    
    total_geral = 0
    pdf.set_font("Arial", size=9)
    for _, row in df_periodo.iterrows():
        status_encerrado = "ENCERRADO" in str(row['STATUS']).upper()
        valor = row['TOTAL'] if status_encerrado else 0
        total_geral += valor
        pdf.cell(20, 8, str(row['O.S']), 1); pdf.cell(60, 8, str(row['CLIENTE']), 1)
        pdf.cell(30, 8, str(row['INICIO']), 1); pdf.cell(30, 8, str(row['FIM']), 1)
        pdf.cell(40, 8, str(row['TIPO']), 1); pdf.cell(40, 8, f"R$ {valor:,.2f}", 1, 1)
    
    pdf.ln(5); pdf.set_font("Arial", 'B', 11); pdf.cell(0, 10, f"FATURAMENTO TOTAL: R$ {total_geral:,.2f}", 0, 1, 'R')
    return pdf.output(dest='S').encode('latin-1', 'ignore')

# --- LOGICA DE TELAS ---
if st.session_state.tela == "HOME":
    st.markdown("<h1 style='text-align: center;'>ZION TECNOLOGIA</h1>", unsafe_allow_html=True)
    if st.button("🔵 ACESSAR SISTEMA", use_container_width=True): st.session_state.tela = "MENU_ICONES"; st.rerun()

elif st.session_state.tela == "MENU_ICONES":
    c1, c2 = st.columns(2)
    if c1.button("⏳ AGENDAMENTO & CADASTRO", use_container_width=True): st.session_state.tela = "AGENDAMENTO"; st.rerun()
    if c2.button("💰 FINANCEIRO", use_container_width=True): st.session_state.tela = "FINANCEIRO"; st.rerun()

elif st.session_state.tela == "AGENDAMENTO":
    if st.button("⬅️ VOLTAR"): st.session_state.tela = "MENU_ICONES"; st.rerun()
    
    # FORMULÁRIO (Limpa após salvar)
    with st.expander("➕ NOVO CADASTRO", expanded=False):
        with st.form("f_cadastro", clear_on_submit=True):
            c1, c2, c3 = st.columns(3)
            cli = c1.text_input("CLIENTE", value="TRANSDOURADA")
            tipo = c1.selectbox("TIPO SERVIÇO", ["ESCOLTA", "VIGILANTE"])
            os_n = c1.text_input("O.S")
            ini = c2.date_input("INÍCIO MISSÃO", format="DD/MM/YYYY")
            fim = c2.date_input("FIM MISSÃO", format="DD/MM/YYYY")
            h_emb = c2.text_input("HORA EMBARQUE")
            emp = c3.text_input("EMPURRADOR")
            cmt = c3.text_input("CMT")
            stt = c3.selectbox("STATUS", ["ANDAMENTO", "ENCERRADO"])
            
            r1, r2, r3 = st.columns(3)
            ori, dest, bal = r1.text_input("LOCAL"), r2.text_input("DESTINO"), r3.text_input("BALSA")
            desc = st.text_area("DESCRIÇÃO")
            ass_n = st.text_input("ASSINATURA (NOME)")

            if st.form_submit_button("✅ SALVAR"):
                dias = (fim - ini).days if (fim - ini).days > 0 else 1
                v_diaria = 1870.0 if tipo == "ESCOLTA" else 970.0
                st.session_state.db_os.append({
                    "O.S": os_n, "INICIO": ini.strftime('%d/%m/%Y'), "FIM": fim.strftime('%d/%m/%Y'),
                    "DT_OBJ": ini, "DIAS": dias, "TIPO": tipo, "TOTAL": dias * v_diaria,
                    "HORA": h_emb, "LOCAL": ori, "EMPURRADOR": emp, "CMT": cmt, "CLIENTE": cli, 
                    "BALSA": bal, "DESTINO": dest, "PEDIDO": "0001", "STATUS": "⏳ ANDAMENTO" if stt == "ANDAMENTO" else "✅ ENCERRADO",
                    "DESCRIÇÃO": desc, "ESCOLTA1": "", "ESCOLTA2": "", "SAIDA": ori, "ASSINATURA": ass_n
                })
                st.rerun()

    # TABELA (Sem Valor Diário)
    if st.session_state.db_os:
        df = pd.DataFrame(st.session_state.db_os)
        cols_show = ["O.S", "INICIO", "FIM", "DIAS", "TIPO", "EMPURRADOR", "CMT", "CLIENTE", "STATUS"]
        st.dataframe(df[cols_show], use_container_width=True, hide_index=True)
        
        for i, row in df.iterrows():
            with st.expander(f"AÇÕES O.S {row['O.S']}"):
                col_ed, col_pr = st.columns(2)
                if col_ed.button(f"🟠 EDITAR O.S {row['O.S']}", key=f"ed_{i}"):
                    st.session_state.editando_idx = i; st.session_state.tela = "EDITAR"; st.rerun()
                
                pdf_bytes = gerar_pdf_os(row.to_dict())
                col_pr.download_button(f"📥 IMPRIMIR O.S {row['O.S']}", data=pdf_bytes, file_name=f"OS_{row['O.S']}.pdf", key=f"pdf_{i}")

elif st.session_state.tela == "FINANCEIRO":
    if st.button("⬅️ VOLTAR"): st.session_state.tela = "MENU_ICONES"; st.rerun()
    st.title("💰 Financeiro")
    
    if st.session_state.db_os:
        df_f = pd.DataFrame(st.session_state.db_os)
        
        # Filtro e Botão Azul
        c_i, c_f, c_b = st.columns([2, 2, 2])
        d_ini = c_i.date_input("Início", datetime.now())
        d_fim = c_f.date_input("Fim", datetime.now())
        
        df_f_filt = df_f[(df_f['DT_OBJ'] >= d_ini) & (df_f['DT_OBJ'] <= d_fim)]
        pdf_rel = gerar_relatorio_financeiro(df_f_filt, d_ini, d_fim)
        
        c_b.markdown("<br>", unsafe_allow_html=True)
        c_b.download_button("🔵 GERAR RELATÓRIO PDF", data=pdf_rel, file_name="Financeiro_Zion.pdf", use_container_width=True)
        
        # Exibição (Valor apenas se encerrado)
        df_f['VALOR EXIBIDO'] = df_f.apply(lambda x: f"R$ {x['TOTAL']:,.2f}" if "ENCERRADO" in x['STATUS'] else "---", axis=1)
        st.table(df_f[["O.S", "CLIENTE", "STATUS", "VALOR EXIBIDO"]])

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
