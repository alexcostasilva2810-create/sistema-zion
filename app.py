import streamlit as st
import pandas as pd
from fpdf import FPDF
import os
from datetime import datetime

# 1. CONFIGURAÇÃO E IDENTIDADE VISUAL
st.set_page_config(page_title="ZION TECNOLOGIA", layout="wide")

# Estilização CSS para botões e tabelas
st.markdown("""
    <style>
    div.stButton > button:first-child { background-color: #f44336; color: white; border-radius: 5px; height: 3em; font-weight: bold; }
    .st-emotion-cache-19rxjzoef { background-color: #4CAF50 !important; color: white !important; font-weight: bold !important; }
    .stDataFrame { border: 1px solid #f44336; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

# 2. ESTRUTURA DE DADOS (LISTA MESTRA)
CAMPOS_MESTRES = [
    "O.S", "PEDIDO", "CLIENTE", "TIPO", "INICIO", "FIM", "HORA", "SAIDA", 
    "EMPURRADOR", "CMT", "ESCOLTA1", "ESCOLTA2", "LOCAL", "DESTINO", "BALSA", "STATUS", "DESCRIÇÃO", "ASSINATURA"
]

# Inicialização do Banco de Dados em Memória
if 'db_os' not in st.session_state: st.session_state.db_os = []
if 'tela' not in st.session_state: st.session_state.tela = "HOME"
if 'exibir_form' not in st.session_state: st.session_state.exibir_form = False

# 3. FUNÇÃO PARA GERAR PDF DA O.S. INDIVIDUAL
def gerar_pdf_os(dados):
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.add_page()
    
    # Tenta carregar a logo no topo do PDF
    if os.path.exists("logo app.jpg"):
        try: pdf.image("logo app.jpg", x=80, y=10, w=45); pdf.ln(30)
        except: pdf.ln(10)
    else:
        pdf.ln(10)
    
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "ORDEM DE SERVIÇO DE ESCOLTA", ln=True, align='C')
    pdf.ln(5)
    
    pdf.set_font("Arial", size=10)
    for campo in CAMPOS_MESTRES:
        if campo not in ["DESCRIÇÃO", "ASSINATURA"]:
            pdf.set_fill_color(240, 240, 240)
            pdf.cell(50, 7, txt=f" {campo}:", border=1, fill=True)
            val = str(dados.get(campo, '---')).encode('latin-1', 'replace').decode('latin-1')
            pdf.cell(140, 7, txt=f" {val}", border=1); pdf.ln()
    
    pdf.ln(5); pdf.set_font("Arial", 'B', 10); pdf.cell(0, 8, "DESCRIÇÃO:", ln=True)
    pdf.set_font("Arial", size=10)
    desc = str(dados.get('DESCRIÇÃO', '---')).encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(0, 7, txt=desc, border=1)
    
    pdf.ln(20)
    pdf.cell(0, 10, "________________________________________________", 0, 1, 'C')
    nome_ass = str(dados.get('ASSINATURA', 'ZION TECNOLOGIA')).encode('latin-1', 'replace').decode('latin-1')
    pdf.cell(0, 5, nome_ass, 0, 1, 'C')
    return pdf.output(dest='S').encode('latin-1', 'ignore')

# 4. BARRA LATERAL (SIDEBAR) COM LOGO
with st.sidebar:
    # Mostra a logo na barra lateral se o arquivo existir
    if os.path.exists("LOGO.PNG"):
        st.image("LOGO.PNG", use_container_width=True)
    
    st.divider()
    if st.button("🏠 MENU PRINCIPAL", use_container_width=True): 
        st.session_state.tela = "MENU_ICONES"
        st.rerun()

# 5. TELAS DO SISTEMA

# TELA HOME (LOGIN/ENTRADA)
if st.session_state.tela == "HOME":
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if os.path.exists("LOGO.PNG"): 
            st.image("LOGO.PNG", use_container_width=True)
        st.markdown("<h1 style='text-align: center;'>SISTEMA DE GESTÃO</h1>", unsafe_allow_html=True)
        if st.button("🔵 ENTRAR NO SISTEMA", use_container_width=True): 
            st.session_state.tela = "MENU_ICONES"
            st.rerun()

# TELA DE MENU (ÍCONES)
elif st.session_state.tela == "MENU_ICONES":
    st.markdown("<h2 style='text-align: center;'>PAINEL DE CONTROLE</h2>", unsafe_allow_html=True)
    st.write("---")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("⏳ AGENDAMENTO / O.S", use_container_width=True):
            st.session_state.tela = "AGENDAMENTO"
            st.rerun()
    with c2:
        if st.button("💰 FINANCEIRO / RELATÓRIOS", use_container_width=True):
            st.session_state.tela = "FINANCEIRO"
            st.rerun()

# TELA DE AGENDAMENTO
elif st.session_state.tela == "AGENDAMENTO":
    st.title("⏳ Agendamento de Escoltas")
    
    # Métricas rápidas
    if st.session_state.db_os:
        df_d = pd.DataFrame(st.session_state.db_os)
        andamento = len(df_d[df_d['STATUS'].str.contains("ANDAMENTO")])
        encerrado = len(df_d[df_d['STATUS'].str.contains("ENCERRADO")])
        m1, m2, m3 = st.columns(3)
        m1.metric("EM ANDAMENTO", andamento)
        m2.metric("ENCERRADAS", encerrado)
        m3.metric("TOTAL GERAL", len(df_d))

    if st.button("🔴 NOVO CADASTRO"):
        st.session_state.exibir_form = not st.session_state.exibir_form
        st.rerun()

    if st.session_state.exibir_form:
        with st.form("f_cadastro", clear_on_submit=True):
            st.subheader("📝 Dados da Nova Operação")
            c1, c2, c3, c4 = st.columns(4)
            os_n = c1.text_input("Nº O.S")
            ped = c2.text_input("PEDIDO")
            cli = c3.text_input("CLIENTE", value="TRANSDOURADA")
            tipo = c4.selectbox("TIPO SERVIÇO", ["ESCOLTA", "VIGILANTE"])
            
            c5, c6, c7, c8 = st.columns(4)
            ini = c5.date_input("INÍCIO", format="DD/MM/YYYY")
            fim = c6.date_input("FIM", format="DD/MM/YYYY")
            h_emb = c7.text_input("HORA EMBARQUE")
            sai = c8.text_input("SAÍDA")
            
            c9, c10, c11, c12 = st.columns(4)
            emp = c9.text_input("EMPURRADOR")
            cmt = c10.text_input("CMT")
            esc1 = c11.text_input("ESCOLTA 1")
            esc2 = c12.text_input("ESCOLTA 2")
            
            c13, c14, c15, c16 = st.columns(4)
            ori = c13.text_input("LOCAL ORIGEM")
            dst = c14.text_input("DESTINO")
            bal = c15.text_input("BALSA")
            stt = c16.selectbox("STATUS", ["ANDAMENTO", "ENCERRADO"])
            
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
                st.session_state.exibir_form = False
                st.rerun()

    # Tabela de visualização
    if st.session_state.db_os:
        df = pd.DataFrame(st.session_state.db_os)
        st.dataframe(df[CAMPOS_MESTRES], use_container_width=True, hide_index=True)
        
        # Gerenciamento individual
        for i, row in df.iterrows():
            with st.expander(f"⚙️ Opções da O.S {row['O.S']}"):
                c_ed, c_pr = st.columns(2)
                if c_ed.button(f"🟠 EDITAR", key=f"ed_{i}"):
                    st.session_state.editando_idx = i
                    st.session_state.tela = "EDITAR"
                    st.rerun()
                
                pdf_b = gerar_pdf_os(row.to_dict())
                c_pr.download_button(f"📥 IMPRIMIR PDF", data=pdf_b, file_name=f"OS_{row['O.S']}.pdf", key=f"pdf_{i}")

# TELA FINANCEIRA
elif st.session_state.tela == "FINANCEIRO":
    st.title("💰 Relatórios Financeiros")
    if st.session_state.db_os:
        df_f = pd.DataFrame(st.session_state.db_os)
        df_f['DT_OBJ'] = pd.to_datetime(df_f['DT_OBJ']).dt.date
        
        st.subheader("📅 Filtrar por Período")
        c1, c2, c3 = st.columns([2, 2, 2])
        data_ini = c1.date_input("De:", value=datetime.now().date().replace(day=1), format="DD/MM/YYYY")
        data_fim = c2.date_input("Até:", format="DD/MM/YYYY")
        
        df_filtrado = df_f[(df_f['DT_OBJ'] >= data_ini) & (df_f['DT_OBJ'] <= data_fim)]
        st.dataframe(df_filtrado[["O.S", "CLIENTE", "TIPO", "INICIO", "FIM", "STATUS"]], use_container_width=True, hide_index=True)
        
        total_p = df_filtrado[df_filtrado['STATUS'].str.contains("ENCERRADO")]['TOTAL'].sum()
        
        st.divider()
        st.metric("SOMA TOTAL DO PERÍODO", f"R$ {total_p:,.2f}")
    else:
        st.info("Nenhum dado cadastrado para gerar faturamento.")

# TELA DE EDIÇÃO
elif st.session_state.tela == "EDITAR":
    idx = st.session_state.editando_idx
    if idx is not None:
        st.title(f"🟠 Editando O.S {st.session_state.db_os[idx]['O.S']}")
        with st.form("f_ed"):
            n_stt = st.selectbox("STATUS", ["ANDAMENTO", "ENCERRADO"], index=0 if "ANDAMENTO" in st.session_state.db_os[idx]['STATUS'] else 1)
            n_desc = st.text_area("DESCRIÇÃO", value=st.session_state.db_os[idx]['DESCRIÇÃO'])
            if st.form_submit_button("💾 SALVAR ALTERAÇÕES"):
                st.session_state.db_os[idx]['STATUS'] = "⏳ ANDAMENTO" if n_stt == "ANDAMENTO" else "✅ ENCERRADO"
                st.session_state.db_os[idx]['DESCRIÇÃO'] = n_desc
                st.session_state.tela = "AGENDAMENTO"
                st.rerun()
        if st.button("❌ CANCELAR"): 
            st.session_state.tela = "AGENDAMENTO"
            st.rerun()
