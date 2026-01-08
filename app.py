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

# --- ESTILO CSS (ROBÔ + AZUL ROYAL TRANSPARENTE) ---
st.markdown(f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(0, 35, 102, 0.7), rgba(0, 35, 102, 0.7)), 
                    url("https://images.unsplash.com/photo-1589254065878-42c9da997008?q=80&w=2070&auto=format&fit=crop");
        background-size: cover; background-position: center; background-attachment: fixed;
    }}
    h1, h2, h3, label, .stMarkdown {{ color: #00ff41 !important; text-shadow: 2px 2px 4px #000; text-align: center; }}
    div.stButton > button {{ border-radius: 8px; font-weight: bold; }}
    .btn-salvar-verde > div > button {{
        background-color: #28a745 !important;
        color: white !important;
        border: none !important;
        width: 100%;
    }}
    .stDataFrame {{ background-color: rgba(15, 23, 42, 0.8); border: 1px solid #00ff41; border-radius: 10px; }}
    </style>
    """, unsafe_allow_html=True)

# --- FUNÇÃO GERAR PDF ---
def gerar_os_pdf(d):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_fill_color(10, 20, 40)
    pdf.rect(0, 0, 210, 40, 'F')
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(190, 10, "ZION TECNOLOGIA - ORDEM DE SERVICO", ln=True, align='C')
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(190, 10, f"O.S NUMERO: {d['os_n']}", ln=True, align='C')
    pdf.ln(10)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", '', 10)
    
    # Detalhamento de todas as colunas no PDF
    for k, v in d.items():
        if k not in ["ID", "dt_raw"]:
            pdf.cell(190, 8, f"{str(k).upper()}: {str(v)}", border=1, ln=True)
    return pdf.output(dest='S').encode('latin-1')

# --- CARREGAR DADOS (Ajustado para DT SAIDA sem acento) ---
def carregar_dados():
    try:
        res = requests.post(f"https://api.notion.com/v1/databases/{DATABASE}/query", headers=headers)
        if res.status_code == 200:
            results = res.json().get("results", [])
            lista = []
            for r in results:
                p = r["properties"]
                
                # Funções de segurança para garantir que o dado retorne mesmo com erro de nome
                def g_t(n): 
                    return p[n]["rich_text"][0]["plain_text"] if n in p and p[n].get("rich_text") else ""
                
                def g_d(n): 
                    return p[n]["date"]["start"] if n in p and p.get(n) and p[n].get("date") else None

                # Mapeamento exato das colunas do seu Notion
                lista.append({
                    "ID": r["id"],
                    "os_n": p["Nº OS"]["title"][0]["plain_text"] if "Nº OS" in p and p["Nº OS"]["title"] else "---",
                    "cli": g_t("CLIENTE"), 
                    "dt_s": g_d("DT SAÍDA"), # Puxa do Notion (AAAA-MM-DD)
                    "emp": g_t("EMPURRADOR"),
                    "bal": g_t("BALSA"),
                    "ped": g_t("PEDIDO"),
                    "h_e": g_t("HORA DE EMBARQUE"),
                    "esc1": g_t("ESCOLTA 1"),
                    "esc2": g_t("ESCOLTA 2"),
                    "loc": g_t("LOCAL"),
                    "dst": g_t("DESTINO"),
                    "ass": g_t("ASSINATURA"),
                    "ini_m": g_d("INÍCIO DA MISSÃO"),
                    "fim_m": g_d("FIM DA MISSÃO"),
                    "sts": p["STATUS"]["select"]["name"] if "STATUS" in p and p["STATUS"].get("select") else "Em Andamento",
                    "obs": g_t("DESCRIÇÃO"), 
                    "v_total": p["VALOR TOTAL"]["number"] if "VALOR TOTAL" in p and p["VALOR TOTAL"].get("number") else 0
                })
            return lista
    except Exception as e:
        st.error(f"Erro ao carregar: {e}")
        return []
    return []

# --- SALVAR NO NOTION (Restaurado com 17 colunas e nomes corretos) ---
def salvar_no_notion(d, page_id=None):
    url = f"https://api.notion.com/v1/pages/{page_id}" if page_id else "https://api.notion.com/v1/pages"
    method = requests.patch if page_id else requests.post
    
    # Montagem do Payload (O que será enviado ao Notion)
    payload = {
        "properties": {
            "Nº OS": {"title": [{"text": {"content": str(d['os_n'])}}]},
            "CLIENTE": {"rich_text": [{"text": {"content": str(d['cli'])}}]},
            "DT SAÍDA": {"date": {"start": d['dt_s'].strftime('%Y-%m-%d')}} if d['dt_s'] else None,
            "EMPURRADOR": {"rich_text": [{"text": {"content": str(d['emp'])}}]},
            "BALSA": {"rich_text": [{"text": {"content": str(d['bal'])}}]},
            "PEDIDO": {"rich_text": [{"text": {"content": str(d['ped'])}}]},
            "HORA DE EMBARQUE": {"rich_text": [{"text": {"content": str(d['h_e'])}}]},
            "ESCOLTA 1": {"rich_text": [{"text": {"content": str(d['esc1'])}}]},
            "ESCOLTA 2": {"rich_text": [{"text": {"content": str(d['esc2'])}}]},
            "LOCAL": {"rich_text": [{"text": {"content": str(d['loc'])}}]},
            "DESTINO": {"rich_text": [{"text": {"content": str(d['dst'])}}]},
            "ASSINATURA": {"rich_text": [{"text": {"content": str(d['ass'])}}]},
            "INÍCIO DA MISSÃO": {"date": {"start": d['ini_m'].strftime('%Y-%m-%d')}} if d['ini_m'] else None,
            "FIM DA MISSÃO": {"date": {"start": d['fim_m'].strftime('%Y-%m-%d')}} if d['fim_m'] else None,
            "STATUS": {"select": {"name": str(d['sts'])}},
            "DESCRIÇÃO": {"rich_text": [{"text": {"content": str(d['obs'])}}]},
            "VALOR TOTAL": {"number": float(str(d['v_total']).replace(',', '.')) if d['v_total'] else 0.0}
        }
    }
    
    if not page_id: 
        payload["parent"] = {"database_id": DATABASE}
        
    res = method(url, headers=headers, json=payload)
    
    # Verifica se deu certo (Status 200 ou 202)
    if res.status_code in [200, 202]:
        return True
    else:
        st.error(f"Erro ao salvar no Notion: {res.text}")
        return False
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
        dt_s = c2.date_input("DATA SAÍDA", value=datetime.strptime(e['dt_s'], '%Y-%m-%d') if e and e['dt_s'] else datetime.now(), format="DD/MM/YYYY")
        cli = c3.text_input("CLIENTE", value=e['cli'] if e else "")
        c4, c5, c6 = st.columns(3)
        emp, bal, ped = c4.text_input("EMPURRADOR", value=e['emp'] if e else ""), c5.text_input("BALSA", value=e['bal'] if e else ""), c6.text_input("PEDIDO", value=e['ped'] if e else "")
        c7, c8, c9 = st.columns(3)
        h_e, esc1, esc2 = c7.text_input("HORA EMBARQUE", value=e['h_e'] if e else ""), c8.text_input("ESCOLTA 1", value=e['esc1'] if e else ""), c9.text_input("ESCOLTA 2", value=e['esc2'] if e else "")
        c10, c11, c12 = st.columns(3)
        loc, dst, ass = c10.text_input("LOCAL", value=e['loc'] if e else ""), c11.text_input("DESTINO", value=e['dst'] if e else ""), c12.text_input("ASSINATURA", value=e['ass'] if e else "")
        c13, c14, c15 = st.columns(3)
        ini_m = c13.date_input("INÍCIO MISSÃO", value=datetime.strptime(e['ini_m'], '%Y-%m-%d') if e and e['ini_m'] else datetime.now(), format="DD/MM/YYYY")
        fim_m = c14.date_input("FIM MISSÃO", value=datetime.strptime(e['fim_m'], '%Y-%m-%d') if e and e['fim_m'] else datetime.now(), format="DD/MM/YYYY")
        sts = c15.selectbox("STATUS", ["Em Andamento", "Encerrado"], index=0 if not e or e['sts'] == "Em Andamento" else 1)
        obs = st.text_area("DESCRIÇÃO", value=e['obs'] if e else "")
        v_total = st.text_input("VALOR TOTAL", value=str(e['v_total']) if e else "0.00")
        st.markdown('<div class="btn-salvar-verde">', unsafe_allow_html=True)
        if st.form_submit_button("✅ SALVAR OPERAÇÃO"):
            dados = {"os_n":os_n, "dt_s":dt_s, "cli":cli, "emp":emp, "bal":bal, "ped":ped, "h_e":h_e, "esc1":esc1, "esc2":esc2, "loc":loc, "dst":dst, "ass":ass, "ini_m":ini_m, "fim_m":fim_m, "sts":sts, "obs":obs, "v_total":v_total}
            if salvar_no_notion(dados, e['ID'] if e else None): navegar("📊 GRADE")
        st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.pagina == "📊 GRADE":
    st.header("📊 AGENDAMENTOS")
    if st.button("⬅️ VOLTAR"): navegar("🏠 HOME")
    dados = carregar_dados()
    if dados:
        for d in dados:
            col_os, col_cli, col_edit, col_print = st.columns([1, 3, 1, 1])
            col_os.write(f"O.S: {d['os_n']}")
            col_cli.write(f"Cli: {d['cli']}")
            if col_edit.button("✏️", key=f"ed_{d['ID']}"):
                st.session_state.edit_data = d
                navegar("📋 CADASTRO")
            col_print.download_button("🖨️", data=gerar_os_pdf(d), file_name=f"OS_{d['os_n']}.pdf", key=f"pr_{d['ID']}")
            st.divider()

elif st.session_state.pagina == "💰 FINANCEIRO":
    st.markdown("<h1>💰 RELATÓRIO FINANCEIRO ZION</h1>", unsafe_allow_html=True)
    if st.button("⬅️ VOLTAR"): navegar("🏠 HOME")
    
    # 1. Filtros de Período
    col_f1, col_f2 = st.columns(2)
    data_ini = col_f1.date_input("Início do Período", datetime.now(), format="DD/MM/YYYY")
    data_fim = col_f2.date_input("Fim do Período", datetime.now(), format="DD/MM/YYYY")

    dados = carregar_dados()
    if dados:
        df = pd.DataFrame(dados)
        
        # Converter colunas para formato de data real para o cálculo
        df['ini_m'] = pd.to_datetime(df['ini_m'], errors='coerce')
        df['fim_m'] = pd.to_datetime(df['fim_m'], errors='coerce')
        df['dt_s'] = pd.to_datetime(df['dt_s'], errors='coerce')

        # --- LÓGICA DE CÁLCULO DE DIAS E VALORES ---
        def processar_financeiro(row):
            try:
                # Calcula a diferença de dias
                if pd.notnull(row['ini_m']) and pd.notnull(row['fim_m']):
                    delta = (row['fim_m'] - row['ini_m']).days
                    qtd_dias = delta + 1 if delta >= 0 else 1 # Mínimo de 1 dia
                else:
                    qtd_dias = 0
                
                # Valor unitário vindo do lançamento
                valor_unitario = float(str(row['v_total']).replace(',', '.')) if row['v_total'] else 0.0
                return pd.Series([qtd_dias, qtd_dias * valor_unitario])
            except:
                return pd.Series([0, 0.0])

        # Aplica o cálculo e cria novas colunas
        df[['DIAS', 'TOTAL_OS']] = df.apply(processar_financeiro, axis=1)

        # Filtrar pelo período selecionado (baseado na Data de Saída)
        mask = (df['dt_s'].dt.date >= data_ini) & (df['dt_s'].dt.date <= data_fim)
        df_f = df.loc[mask].copy()

        # Exibir Métricas de Resumo
        c_m1, c_m2 = st.columns(2)
        c_m1.metric("Qtd. de O.S no Período", len(df_f))
        c_m2.metric("Faturamento Total (R$)", f"R$ {df_f['TOTAL_OS'].sum():,.2f}")

        # --- TABELA VISUAL ---
        st.write("### 📋 Detalhamento de Cobrança")
        # Preparar tabela para exibição
        df_view = df_f[['os_n', 'cli', 'DIAS', 'v_total', 'TOTAL_OS', 'sts']].copy()
        df_view.columns = ['Nº O.S', 'CLIENTE', 'DIAS DE OP.', 'VALOR DIÁRIA (R$)', 'TOTAL O.S (R$)', 'STATUS']
        
        st.dataframe(df_view, use_container_width=True, hide_index=True)

        # --- BOTÃO DE RELATÓRIO PDF ---
        def gerar_pdf_financeiro(df_rel, d1, d2):
            pdf = FPDF()
            pdf.add_page()
            # Cabeçalho Zion
            pdf.set_fill_color(0, 35, 102) # Azul Royal
            pdf.rect(0, 0, 210, 45, 'F')
            pdf.set_text_color(255, 255, 255)
            pdf.set_font("Arial", 'B', 16)
            pdf.cell(190, 15, "ZION TECNOLOGIA - RELATORIO FINANCEIRO", ln=True, align='C')
            pdf.set_font("Arial", '', 10)
            pdf.cell(190, 10, f"PERIODO: {d1.strftime('%d/%m/%Y')} A {d2.strftime('%d/%m/%Y')}", ln=True, align='C')
            
            pdf.ln(15)
            pdf.set_text_color(0, 0, 0)
            pdf.set_font("Arial", 'B', 8)
            # Títulos da Tabela no PDF
            pdf.cell(20, 10, "O.S", 1, 0, 'C')
            pdf.cell(70, 10, "CLIENTE", 1, 0, 'C')
            pdf.cell(20, 10, "DIAS", 1, 0, 'C')
            pdf.cell(40, 10, "VL. DIARIA", 1, 0, 'C')
            pdf.cell(40, 10, "TOTAL O.S", 1, 1, 'C')
            
            pdf.set_font("Arial", '', 8)
            for _, r in df_rel.iterrows():
                pdf.cell(20, 8, str(r['Nº O.S']), 1, 0, 'C')
                pdf.cell(70, 8, str(r['CLIENTE'])[:35], 1, 0, 'L')
                pdf.cell(20, 8, str(int(r['DIAS DE OP.'])), 1, 0, 'C')
                pdf.cell(40, 8, f"{float(r['VALOR DIÁRIA (R$)']):,.2f}", 1, 0, 'R')
                pdf.cell(40, 8, f"{r['TOTAL O.S (R$)']:,.2f}", 1, 1, 'R')
            
            pdf.ln(5)
            total_geral = df_rel['TOTAL O.S (R$)'].sum()
            pdf.set_font("Arial", 'B', 10)
            pdf.cell(190, 10, f"VALOR TOTAL DO PERIODO: R$ {total_geral:,.2f}", 0, 1, 'R')
            
            return pdf.output(dest='S').encode('latin-1')

        pdf_data = gerar_pdf_financeiro(df_view, data_ini, data_fim)
        st.download_button(
            label="📑 GERAR PDF DO FINANCEIRO",
            data=pdf_data,
            file_name=f"Financeiro_Zion_{data_ini}.pdf",
            mime="application/pdf"
        )
    else:
        st.warning("Nenhum dado encontrado para o período selecionado.")
