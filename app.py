import streamlit as st
import pandas as pd
from fpdf import FPDF
import os
from datetime import datetime

# 1. CONFIGURAÇÃO E IDENTIDADE VISUAL
st.set_page_config(page_title="ZION TECNOLOGIA", layout="wide")

st.markdown("""
    <style>
    /* Botão Novo Cadastro - Vermelho */
    div.stButton > button:first-child { background-color: #f44336; color: white; border-radius: 5px; height: 3em; font-weight: bold; }
    /* Botão Salvar dentro do formulário - Verde */
    .st-emotion-cache-19rxjzoef { background-color: #4CAF50 !important; color: white !important; font-weight: bold !important; }
    /* Estilo das tabelas */
    .stDataFrame { border: 1px solid #f44336; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

# 2. ESTRUTURA DE DADOS (LISTA MESTRA - NÃO REMOVER)
# Garante que todos os campos apareçam no formulário, tabela e PDF
CAMPOS_MESTRES = [
    "O.S", "PEDIDO", "CLIENTE", "TIPO", "INICIO", "FIM", "HORA", "SAIDA", 
    "EMPURRADOR", "CMT", "ESCOLTA1", "ESCOLTA2", "LOCAL", "DESTINO", "BALSA", "STATUS", "DESCRIÇÃO", "ASSINATURA"
]

if 'db_os' not in st.session_state: st.session_state.db_os = []
if 'tela' not in st.session_state: st.session_state.tela = "HOME"
if 'exibir_form' not in st.session_state: st.session_state.exibir_form = False

# 3. GERADOR DE PDF (O.S. COMPLETA)
def gerar_pdf_os(dados):
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.add_page()
    
    # Logo
    if os.path.exists("logo app.jpg"):
        try: pdf.image("logo app.jpg", x=80, y=10, w=45); pdf.ln(30)
        except: pdf.ln(10)
    
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "ORDEM DE SERVIÇO DE ESCOLTA", ln=True, align='C')
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(0, 7, f"CLIENTE: {dados.get('CLIENTE')} | O.S: {dados.get('O.S')}", ln=True, align='C')
    pdf.ln(5); pdf.line(10, pdf.get_y(), 200, pdf.get_y()); pdf.ln(5)

    pdf.set_font("Arial", size=10)
    # Loop pelos campos mestres para garantir que nada fique de fora
    for campo in CAMPOS_MESTRES:
        if campo not in ["DESCRIÇÃO", "ASSINATURA"]:
            pdf.set_fill_color(240, 240, 240)
            pdf.cell(50, 7, txt=f" {campo}:", border=1, fill=True)
            val = str(dados.get(campo, '---')).encode('latin-1', 'replace').decode('latin-1')
            pdf.cell(140, 7, txt=f" {val}", border=1); pdf.ln()
    
    # Descrição
    pdf.ln(5); pdf.set_font("Arial", 'B', 10); pdf.cell(0, 8, "DESCRIÇÃO:", ln=True)
    pdf.set_font("Arial", size=10)
    desc = str(dados.get('DESCRIÇÃO', '---')).encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(0, 7, txt=desc, border=1)
    
    # Assinatura (Linha e Nome)
    pdf.ln(20)
    pdf.cell(0, 10, "________________________________________________", 0, 1, 'C')
    pdf.set_font("Arial", 'B', 10)
    nome_ass = str(dados.get('ASSINATURA', 'ZION TECNOLOGIA')).encode('latin-1', 'replace').decode('latin-1')
    pdf.cell(0, 5, nome_ass, 0, 1, 'C')
    
    return pdf.output(dest='S').encode('latin-1', 'ignore')

# 4. INTERFACE E NAVEGAÇÃO
with st.sidebar:
    if os.path.exists("LOGO.PNG"):
        if st.button("🏠 MENU PRINCIPAL", use_container_width=True): 
            st.session_state.tela = "MENU_ICONES"; st.rerun()
        st.image("LOGO.PNG", use_container_width=True)

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
    # Dashboard de Controle
    if st.session_state.db_os:
        df_d = pd.DataFrame(st.session_state.db_os)
        a = len(df_d[df_d['STATUS'].str.contains("ANDAMENTO")])
        f = len(df_d[df_d['STATUS'].str.contains("ENCERRADO")])
        m1, m2, m3 = st.columns(3)
        m1.metric("O.S. EM ANDAMENTO", a)
        m2.metric("O.S. ENCERRADAS", f)
        m3.metric("TOTAL DE OPERAÇÕES", len(df_d))

    # Botão de Cadastro (Vermelho)
    if st.button("🔴 NOVO CADASTRO"):
        st.session_state.exibir_form = not st.session_state.exibir_form

    if st.session_state.exibir_form:
        with st.form("f_cadastro", clear_on_submit=True):
            st.subheader("📝 Preencher Ordem de Serviço")
            c1, c2, c3, c4 = st.columns(4)
            os_n, ped = c1.text_input("Nº O.S"), c2.text_input("PEDIDO")
            cli = c3.text_input("CLIENTE", value="TRANSDOURADA")
            tipo = c4.selectbox("TIPO SERVIÇO", ["ESCOLTA", "VIGILANTE"])
            
            c5, c6, c7, c8 = st.columns(4)
            ini = c5.date_input("INÍCIO", format="DD/MM/YYYY")
            fim = c6.date_input("FIM", format="DD/MM/YYYY")
            h_emb, sai = c7.text_input("HORA EMBARQUE"), c8.text_input("SAÍDA")
            
            c9, c10, c11, c12 = st.columns(4)
            emp, cmt = c9.text_input("EMPURRADOR"), c10.text_input("CMT")
            esc1, esc2 = c11.text_input("ESCOLTA 1"), c12.text_input("ESCOLTA 2")
            
            c13, c14, c15, c16 = st.columns(4)
            ori, dst = c13.text_input("LOCAL ORIGEM"), c14.text_input("DESTINO")
            bal, stt = c15.text_input("BALSA"), c16.selectbox("STATUS", ["ANDAMENTO", "ENCERRADO"])
            
            desc = st.text_area("DESCRIÇÃO")
            ass = st.text_input("ASSINATURA (Nome no PDF)")

            if st.form_submit_button("✅ SALVAR OPERAÇÃO"):
                dias = (fim - ini).days if (fim - ini).days > 0 else 1
                v_dia = 1870.0 if tipo == "ESCOLTA" else 970.0
                st.session_state.db_os.append({
                    "O.S": os_n, "PEDIDO": ped, "CLIENTE": cli, "TIPO": tipo, "INICIO": ini.strftime('%d/%m/%Y'),
                    "FIM": fim.strftime('%d/%m/%Y'), "HORA": h_emb, "SAIDA": sai, "EMPURRADOR": emp,
                    "CMT": cmt, "ESCOLTA1": esc1, "ESCOLTA2": esc2, "LOCAL": ori, "DESTINO": dst,
                    "BALSA": bal, "STATUS": "⏳ ANDAMENTO" if stt == "ANDAMENTO" else "✅ ENCERRADO",
                    "DESCRIÇÃO": desc, "ASSINATURA": ass, "DIAS": dias, "TOTAL": dias * v_dia, "DT_OBJ": ini
                })
                st.session_state.exibir_form = False; st.rerun()

    # Exibição da Tabela com todos os campos da Lista Mestra
    if st.session_state.db_os:
        df = pd.DataFrame(st.session_state.db_os)
        st.dataframe(df[CAMPOS_MESTRES], use_container_width=True, hide_index=True)
        
        for i, row in df.iterrows():
            with st.expander(f"⚙️ GERENCIAR O.S {row['O.S']}"):
                c_ed, c_pr = st.columns(2)
                if c_ed.button(f"🟠 EDITAR", key=f"ed_{i}"):
                    st.session_state.editando_idx = i; st.session_state.tela = "EDITAR"; st.rerun()
                pdf_b = gerar_pdf_os(row.to_dict())
                c_pr.download_button(f"📥 IMPRIMIR PDF", data=pdf_b, file_name=f"OS_{row['O.S']}.pdf", key=f"pdf_{i}")
 elif st.session_state.tela == "FINANCEIRO":
    st.title("💰 Relatórios Financeiros")
    
    if st.session_state.db_os:
        df_f = pd.DataFrame(st.session_state.db_os)
        df_f['DT_OBJ'] = pd.to_datetime(df_f['DT_OBJ']).dt.date
        
        st.subheader("📅 Selecionar Período para o Relatório")
        c1, c2, c3 = st.columns([2, 2, 2])
        data_ini = c1.date_input("De:", value=datetime.now().date().replace(day=1), format="DD/MM/YYYY")
        data_fim = c2.date_input("Até:", format="DD/MM/YYYY")
        
        # Filtrar dados
        df_filtrado = df_f[(df_f['DT_OBJ'] >= data_ini) & (df_f['DT_OBJ'] <= data_fim)]
        
        # Tabela limpa na tela
        st.dataframe(df_filtrado[["O.S", "CLIENTE", "TIPO", "INICIO", "FIM", "STATUS"]], use_container_width=True, hide_index=True)
        
        # Cálculo do total do período
        total_p = df_filtrado[df_filtrado['STATUS'].str.contains("ENCERRADO")]['TOTAL'].sum()

        def gerar_pdf_financeiro(df, total):
            pdf = FPDF(orientation='L', unit='mm', format='A4')
            pdf.add_page()
            pdf.set_font("Arial", 'B', 16)
            pdf.cell(0, 10, "RELATÓRIO FINANCEIRO ZION", ln=True, align='C')
            pdf.set_font("Arial", size=10)
            pdf.cell(0, 8, f"Período: {data_ini.strftime('%d/%m/%Y')} a {data_fim.strftime('%d/%m/%Y')}", ln=True, align='C')
            pdf.ln(5)
            
            # Cabeçalho do PDF
            pdf.set_fill_color(220, 220, 220)
            pdf.set_font("Arial", 'B', 9)
            pdf.cell(20, 8, "O.S", 1, 0, 'C', True)
            pdf.cell(50, 8, "CLIENTE", 1, 0, 'C', True)
            pdf.cell(30, 8, "TIPO", 1, 0, 'C', True)
            pdf.cell(30, 8, "INÍCIO", 1, 0, 'C', True)
            pdf.cell(30, 8, "FIM", 1, 0, 'C', True)
            pdf.cell(20, 8, "DIAS", 1, 0, 'C', True)
            pdf.cell(40, 8, "TOTAL", 1, 1, 'C', True)
            
            pdf.set_font("Arial", size=9)
            for _, r in df.iterrows():
                pdf.cell(20, 7, str(r['O.S']), 1, 0, 'C')
                pdf.cell(50, 7, str(r['CLIENTE'])[:25], 1)
                pdf.cell(30, 7, str(r['TIPO']), 1, 0, 'C')
                pdf.cell(30, 7, str(r['INICIO']), 1, 0, 'C')
                pdf.cell(30, 7, str(r['FIM']), 1, 0, 'C')
                pdf.cell(20, 7, str(r['DIAS']), 1, 0, 'C')
                v = f"R$ {r['TOTAL']:,.2f}" if "ENCERRADO" in r['STATUS'] else "---"
                pdf.cell(40, 7, v, 1, 1, 'R')
            
            pdf.ln(5)
            pdf.set_font("Arial", 'B', 12)
            pdf.cell(0, 10, f"VALOR TOTAL: R$ {total:,.2f}", ln=True, align='R')
            return pdf.output(dest='S').encode('latin-1', 'ignore')

        if c3.button("📊 GERAR RELATÓRIO PDF"):
            pdf_rel = gerar_pdf_financeiro(df_filtrado, total_p)
            st.download_button("📥 BAIXAR PDF", data=pdf_rel, file_name="Relatorio_Financeiro.pdf", mime="application/pdf")
        
        st.divider()
        st.metric("SOMA TOTAL (PERÍODO)", f"R$ {total_p:,.2f}")
    else:
        st.info("Nenhuma O.S. para processar.")
