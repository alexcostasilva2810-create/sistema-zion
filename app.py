import streamlit as st
import requests
import pandas as pd
from fpdf import FPDF
from datetime import datetime
import io

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Zion Tecnologia - Gestão O.S", layout="wide")

# --- CONEXÃO NOTION ---
TOKEN = st.secrets["notion"]["token"].replace('"', '').strip()
DATABASE = st.secrets["notion"]["database_id"].replace('"', '').strip()

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

# --- ESTILO CSS (ROBÔ ANDROIDE + AZUL ROYAL TRANSPARENTE) ---
st.markdown(f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(0, 35, 102, 0.7), rgba(0, 35, 102, 0.7)), 
                    url("https://images.unsplash.com/photo-1589254065878-42c9da997008?q=80&w=2070&auto=format&fit=crop");
        background-size: cover; background-position: center; background-attachment: fixed;
    }}
    h1, h2, h3, label, .stMarkdown {{ color: #00ff41 !important; text-shadow: 2px 2px 4px #000; text-align: center; }}
    div.stButton > button {{ border-radius: 8px; font-weight: bold; }}
    /* Botão Salvar em Verde */
    .btn-salvar-verde > div > button {{
        background-color: #28a745 !important;
        color: white !important;
        border: none !important;
        width: 100%;
    }}
    .stDataFrame {{ background-color: rgba(15, 23, 42, 0.8); border: 1px solid #00ff41; border-radius: 10px; }}
    </style>
    """, unsafe_allow_html=True)

# --- FUNÇÃO GERAR PDF (ESTILO ZION) ---
def gerar_os_pdf(d):
    pdf = FPDF()
    pdf.add_page()
    
    # Cabeçalho Escuro
    pdf.set_fill_color(10, 20, 40)
    pdf.rect(0, 0, 210, 40, 'F')
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(190, 10, "ZION TECNOLOGIA - ORDEM DE SERVICO", ln=True, align='C')
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(190, 10, f"O.S NUMERO: {d['os_n']}", ln=True, align='C')
    
    pdf.ln(10)
    pdf.set_text_color(0, 0, 0)
    
    # Tabela de Informações (Simulando o layout da imagem)
    def criar_bloco(titulo, dados):
        pdf.set_fill_color(230, 230, 230)
        pdf.set_font("Arial", 'B', 10)
        pdf.cell(190, 8, titulo, border=1, ln=True, fill=True)
        pdf.set_font("Arial", '', 9)
        for k, v in dados.items():
            pdf.cell(95, 8, f"{k}: {v}", border=1)
            if list(dados.keys()).index(k) % 2 != 0: pdf.ln()
        pdf.ln(5)

    criar_bloco("INFORMACOES GERAIS", {"CLIENTE": d['cli'], "DATA SAIDA": d['dt_s'], "ORIGEM": d['loc'], "DESTINO": d['dst']})
    criar_bloco("DETALHES DA BALSA", {"EMPURRADOR": d['emp'], "BALSA": d['bal'], "PEDIDO": d['ped'], "HORA EMBARQUE": d['h_e']})
    criar_bloco("EQUIPE E MISSÃO", {"ESCOLTA 1": d['esc1'], "ESCOLTA 2": d['esc2'], "INICIO": d['ini_m'], "FIM": d['fim_m']})
    
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(190, 8, "DESCRICAO DOS SERVICOS", border=1, ln=True, fill=True)
    pdf.set_font("Arial", '', 9)
    pdf.multi_cell(190, 8, d['obs'] or "Nenhuma descrição informada.", border=1)
    
    pdf.ln(20)
    pdf.cell(95, 10, "__________________________", ln=0, align='C')
    pdf.cell(95, 10, "__________________________", ln=1, align='C')
    pdf.cell(95, 5, "ASSINATURA RESPONSAVEL", ln=0, align='C')
    pdf.cell(95, 5, "ZION TECNOLOGIA", ln=1, align='C')
    
    return pdf.output(dest='S').encode('latin-1')

# --- LOGICA DE DADOS (MANTER FUNÇÕES ANTERIORES) ---
def carregar_dados():
    try:
        res = requests.post(f"https://api.notion.com/v1/databases/{DATABASE}/query", headers=headers)
        if res.status_code == 200:
            results = res.json().get("results", [])
            lista = []
            for r in results:
                p = r["properties"]
                def g_t(n): return p[n]["rich_text"][0]["plain_text"] if n in p and p[n]["rich_text"] else ""
                def g_d(n): return p[n]["date"]["start"] if n in p and p[n]["date"] else ""
                
                lista.append({
                    "ID": r["id"],
                    "os_n": p["Nº OS"]["title"][0]["plain_text"] if p["Nº OS"]["title"] else "---",
                    "cli": g_t("CLIENTE"), "dt_s": g_d("DT SAÍDA"), "emp": g_t("EMPURRADOR"),
                    "bal": g_t("BALSA"), "ped": g_t("PEDIDO"), "h_e": g_t("HORA DE EMBARQUE"),
                    "esc1": g_t("ESCOLTA 1"), "esc2": g_t("ESCOLTA 2"), "loc": g_t("LOCAL"),
                    "dst": g_t("DESTINO"), "ass": g_t("ASSINATURA RESPONSÁVEL"),
                    "ini_m": g_d("INÍCIO DA MISSÃO"), "fim_m": g_d("FIM DA MISSÃO"),
                    "sts": p["STATUS"]["select"]["name"] if "STATUS" in p and p["STATUS"]["select"] else "Em Andamento",
                    "obs": g_t("DESCRIÇÃO"), "v_total": p["VALOR TOTAL"]["number"] if "VALOR TOTAL" in p else 0
                })
            return lista
    except: return []

def salvar_no_notion(d, page_id=None):
    url = f"https://api.notion.com/v1/pages/{page_id}" if page_id else "https://api.notion.com/v1/pages"
    method = requests.patch if page_id else requests.post
    payload = {
        "properties": {
            "Nº OS": {"title": [{"text": {"content": str(d['os_n'])}}]},
            "CLIENTE": {"rich_text": [{"text": {"content": str(d['cli'])}}]},
            "DT SAÍDA": {"date": {"start": str(d['dt_s'])}} if d['dt_s'] else None,
            "EMPURRADOR": {"rich_text": [{"text": {"content": str(d['emp'])}}]},
            "BALSA": {"rich_text": [{"text": {"content": str(d['bal'])}}]},
            "PEDIDO": {"rich_text": [{"text": {"content": str(d['ped'])}}]},
            "HORA DE EMBARQUE": {"rich_text": [{"text": {"content": str(d['h_e'])}}]},
            "ESCOLTA 1": {"rich_text": [{"text": {"content": str(d['esc1'])}}]},
            "ESCOLTA 2": {"rich_text": [{"text": {"content": str(d['esc2'])}}]},
            "LOCAL": {"rich_text": [{"text": {"content": str(d['loc'])}}]},
            "DESTINO": {"rich_text": [{"text": {"content": str(d['dst'])}}]},
            "ASSINATURA": {"rich_text": [{"text": {"content": str(d['ass'])}}]},
            "INÍCIO DA MISSÃO": {"date": {"start": str(d['ini_m'])}} if d['ini_m'] else None,
            "FIM DA MISSÃO": {"date": {"start": str(d['fim_m'])}} if d['fim_m'] else None,
            "STATUS": {"select": {"name": str(d['sts'])}},
            "DESCRIÇÃO": {"rich_text": [{"text": {"content": str(d['obs'])}}]},
            "VALOR TOTAL": {"number": float(d['v_total'])}
        }
    }
    if not page_id: payload["parent"] = {"database_id": DATABASE}
    res = method(url, headers=headers, json=payload)
    return res.status_code in [200, 202]

# --- NAVEGAÇÃO ---
if "pagina" not in st.session_state: st.session_state.pagina = "🏠 HOME"
if "edit_data" not in st.session_state: st.session_state.edit_data = None
def navegar(p): st.session_state.pagina = p; st.rerun()

# --- TELAS ---
if st.session_state.pagina == "🏠 HOME":
    st.markdown("<h1>SISTEMA ZION - CONTROLE DE VIGILÂNCIA</h1>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    if c1.button("📋 NOVO LANÇAMENTO"): st.session_state.edit_data = None; navegar("📋 CADASTRO")
    if c2.button("📊 VER AGENDAMENTOS"): navegar("📊 GRADE")
    if c3.button("💰 FINANCEIRO"): navegar("💰 FINANCEIRO")

elif st.session_state.pagina == "📋 CADASTRO":
    e = st.session_state.edit_data
    st.header("✏️ EDITAR O.S" if e else "📝 NOVO REGISTRO")
    if st.button("⬅️ VOLTAR"): navegar("🏠 HOME")
    
    with st.form("form_os"):
        c1, c2, c3 = st.columns(3)
        os_n = c1.text_input("Nº O.S", value=e['os_n'] if e else "")
        dt_s = c2.date_input("DATA SAÍDA", value=datetime.strptime(e['dt_s'], '%Y-%m-%d') if e and e['dt_s'] else datetime.now())
        cli = c3.text_input("CLIENTE", value=e['cli'] if e else "")
        
        c4, c5, c6 = st.columns(3)
        emp, bal, ped = c4.text_input("EMPURRADOR", value=e['emp'] if e else ""), c5.text_input("BALSA", value=e['bal'] if e else ""), c6.text_input("PEDIDO", value=e['ped'] if e else "")
        
        c7, c8, c9 = st.columns(3)
        h_e, esc1, esc2 = c7.text_input("HORA EMBARQUE", value=e['h_e'] if e else ""), c8.text_input("ESCOLTA 1", value=e['esc1'] if e else ""), c9.text_input("ESCOLTA 2", value=e['esc2'] if e else "")
        
        c10, c11, c12 = st.columns(3)
        loc, dst, ass = c10.text_input("LOCAL (ORIGEM)", value=e['loc'] if e else ""), c11.text_input("DESTINO", value=e['dst'] if e else ""), c12.text_input("ASSINATURA RESP.", value=e['ass'] if e else "")
        
        c13, c14, c15 = st.columns(3)
        ini_m = c13.date_input("INÍCIO MISSÃO", value=datetime.strptime(e['ini_m'], '%Y-%m-%d') if e and e['ini_m'] else datetime.now())
        fim_m = c14.date_input("FIM MISSÃO", value=datetime.strptime(e['fim_m'], '%Y-%m-%d') if e and e['fim_m'] else datetime.now())
        sts = c15.selectbox("STATUS", ["Em Andamento", "Encerrado"], index=0 if not e or e['sts'] == "Em Andamento" else 1)
        
        obs = st.text_area("DESCRIÇÃO / OBSERVAÇÕES", value=e['obs'] if e else "")
        v_total = st.text_input("VALOR TOTAL", value=str(e['v_total']) if e else "0.0")

        # Botão Verde de Salvar
        st.markdown('<div class="btn-salvar-verde">', unsafe_allow_html=True)
        btn_txt = "✅ SALVAR EDIÇÃO" if e else "✅ SALVAR REGISTRO"
        if st.form_submit_button(btn_txt):
            dados = {"os_n":os_n, "dt_s":dt_s, "cli":cli, "emp":emp, "bal":bal, "ped":ped, "h_e":h_e, "esc1":esc1, "esc2":esc2, "loc":loc, "dst":dst, "ass":ass, "ini_m":ini_m, "fim_m":fim_m, "sts":sts, "obs":obs, "v_total":v_total}
            if salvar_no_notion(dados, e['ID'] if e else None): navegar("📊 GRADE")
        st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.pagina == "📊 GRADE":
    st.header("📊 AGENDAMENTOS EM TEMPO REAL")
    if st.button("⬅️ VOLTAR"): navegar("🏠 HOME")
    dados = carregar_dados()
    if dados:
        for d in dados:
            with st.container():
                # Layout de linha com ícones
                col_os, col_cli, col_status, col_edit, col_print = st.columns([1, 3, 2, 1, 1])
                col_os.write(f"**O.S:** {d['os_n']}")
                col_cli.write(f"**Cliente:** {d['cli']}")
                col_status.write(f"**Status:** {d['sts']}")
                
                # Botão Lápis (Edição)
                if col_edit.button(f"✏️", key=f"edit_{d['ID']}", help="Editar O.S"):
                    st.session_state.edit_data = d
                    navegar("📋 CADASTRO")
                
                # Botão Impressora (PDF)
                pdf_bytes = gerar_os_pdf(d)
                col_print.download_button(
                    label="🖨️",
                    data=pdf_bytes,
                    file_name=f"OS_{d['os_n']}.pdf",
                    mime="application/pdf",
                    key=f"print_{d['ID']}",
                    help="Imprimir O.S"
                )
                st.divider()
    else:
        st.info("Nenhum agendamento encontrado.")

elif st.session_state.pagina == "💰 FINANCEIRO":
    st.header("💰 RELATÓRIO FINANCEIRO")
    if st.button("⬅️ VOLTAR"): navegar("🏠 HOME")
    # ... (Mantenha sua lógica de faturamento aqui)
