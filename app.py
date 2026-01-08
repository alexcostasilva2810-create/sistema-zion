import streamlit as st
import requests
import pandas as pd
from fpdf import FPDF
from datetime import datetime
import io

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Zion Tecnologia - Gestão O.S", layout="wide")

# --- SISTEMA DE NAVEGAÇÃO (Adicionado para evitar erros) ---
if 'pagina' not in st.session_state:
    st.session_state.pagina = "🏠 HOME"

def navegar(destino):
    st.session_state.pagina = destino
    st.rerun()
# ----------------------------------------------------------
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
# Certifique-se que esta função navegar esteja no topo do seu arquivo app.py
def navegar(pagina):
    st.session_state.pagina = pagina
    st.rerun()

if st.session_state.pagina == "🏠 HOME":
    # Fundo Azul Royal Leve (conforme solicitado)
    st.markdown("""
        <style>
        .stApp { background: linear-gradient(135deg, #e0e8f9 0%, #f0f4ff 100%); }
        .card { background: white; padding: 20px; border-radius: 15px; text-align: center; border: 1px solid #ddd; }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<h1 style='text-align:center; color:#002366;'>ZION - GESTÃO DE ESCOLTA</h1>", unsafe_allow_html=True)

    # Usar colunas que se empilham no celular
    c1, c2, c3 = st.columns([1,1,1])
    
    with c1:
        st.markdown('<div class="card">🤖<br><b>CADASTRO</b></div>', unsafe_allow_html=True)
        if st.button("NOVO LANÇAMENTO", use_container_width=True): navegar("📋 CADASTRO")
    
    with c2:
        st.markdown('<div class="card">📅<br><b>GRADE</b></div>', unsafe_allow_html=True)
        if st.button("VER AGENDAMENTOS", use_container_width=True): navegar("📊 GRADE")
        
    with c3:
        st.markdown('<div class="card">📈<br><b>FINANCEIRO</b></div>', unsafe_allow_html=True)
        if st.button("ESTRATÉGICO", use_container_width=True): navegar("💰 FINANCEIRO")
    # 3. Barra de Status no rodapé
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.info(f"✅ Sistema Zion Conectado | {datetime.now().strftime('%d/%m/%Y')} | Todos os módulos operacionais.")

elif st.session_state.pagina == "📋 CADASTRO":
    e = st.session_state.edit_data
    st.header("✏️ EDITAR O.S" if e else "📝 NOVO REGISTRO")
    if st.button("⬅️ VOLTAR"): navegar("🏠 HOME")
    
    with st.form("form_os", clear_on_submit=True):
        c1, c2, c3 = st.columns(3)
        os_n = c1.text_input("Nº O.S", value=e['os_n'] if e else "")
        dt_s = c2.date_input("DATA SAÍDA", value=datetime.strptime(e['dt_s'], '%Y-%m-%d') if e and e['dt_s'] else datetime.now(), format="DD/MM/YYYY")
        cli = c3.text_input("CLIENTE", value=e['cli'] if e else "")
        
        c4, c5, c6 = st.columns(3)
        emp = c4.text_input("EMPURRADOR", value=e['emp'] if e else "")
        bal = c5.text_input("BALSA", value=e['bal'] if e else "")
        ped = c6.text_input("PEDIDO", value=e['ped'] if e else "")
        
        c7, c8, c9 = st.columns(3)
        h_e = c7.text_input("HORA EMBARQUE", value=e['h_e'] if e else "")
        esc1 = c8.text_input("ESCOLTA 1", value=e['esc1'] if e else "")
        esc2 = c9.text_input("ESCOLTA 2", value=e['esc2'] if e else "")
        
        c10, c11, c12 = st.columns(3)
        loc = c10.text_input("LOCAL (ORIGEM)", value=e['loc'] if e else "")
        dst = c11.text_input("DESTINO", value=e['dst'] if e else "")
        ass = c12.text_input("ASSINATURA RESP.", value=e['ass'] if e else "")
        
        c13, c14, c15 = st.columns(3)
        ini_m = c13.date_input("INÍCIO MISSÃO", value=datetime.strptime(e['ini_m'], '%Y-%m-%d') if e and e['ini_m'] else datetime.now(), format="DD/MM/YYYY")
        fim_m = c14.date_input("FIM MISSÃO", value=datetime.strptime(e['fim_m'], '%Y-%m-%d') if e and e['fim_m'] else datetime.now(), format="DD/MM/YYYY")
        sts = c15.selectbox("STATUS", ["Em Andamento", "Encerrado"], index=0 if not e or e['sts'] == "Em Andamento" else 1)
        
        # --- NOVOS CAMPOS OPERACIONAIS ---
        st.divider()
        c16, c17 = st.columns(2)
        # Seleção que definirá o valor automaticamente no financeiro
        modalidade = c16.selectbox("TIPO DE SERVIÇO", ["ESCOLTA", "VIGILÂNCIA"], index=0)
        # Campo para anexar comprovantes
        arquivo_despesa = c17.file_uploader("CARREGAR COMPROVANTES DE DESPESAS", type=['png', 'jpg', 'jpeg', 'pdf'], help="Anexe notas de combustível, alimentação, etc.")
        
        obs = st.text_area("DESCRIÇÃO / OBSERVAÇÕES", value=e['obs'] if e else "")

        st.markdown('<div class="btn-salvar-verde">', unsafe_allow_html=True)
        if st.form_submit_button("✅ SALVAR REGISTRO"):
            dados = {
                "os_n":os_n, "dt_s":dt_s, "cli":cli, "emp":emp, "bal":bal, "ped":ped, 
                "h_e":h_e, "esc1":esc1, "esc2":esc2, "loc":loc, "dst":dst, "ass":ass, 
                "ini_m":ini_m, "fim_m":fim_m, "sts":sts, "obs":obs, 
                "modalidade": modalidade,
                "v_total": 0 # Valor será definido via regra no Financeiro
            }
            if salvar_no_notion(dados, e['ID'] if e else None): 
                st.success("Dados salvos com sucesso!")
                navegar("📊 GRADE")
        st.markdown('</div>', unsafe_allow_html=True)
elif st.session_state.pagina == "📊 GRADE":
    st.markdown("<h1>ORDEM DE SERVIÇOS 🚢</h1>", unsafe_allow_html=True)
    if st.button("⬅️ VOLTAR"): navegar("🏠 HOME")
    
    dados = carregar_dados()
    if dados:
        df = pd.DataFrame(dados)
        
        # --- TABELA VISÍVEL NA TELA ---
        st.write("### 📋 Lista de Operações")
        df_grade = df[['os_n', 'dt_s', 'cli', 'sts']].copy()
        df_grade.columns = ['Nº O.S', 'DATA SAÍDA', 'CLIENTE', 'STATUS']
        st.dataframe(df_grade, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        st.write("### 🛠️ Ações por Registro")

        # Cabeçalho da Lista de Ações
        h1, h2, h3, h4 = st.columns([1, 4, 1, 1])
        h1.write("**O.S**")
        h2.write("**CLIENTE**")
        h3.write("**EDITAR**")
        h4.write("**IMPRIMIR**")

        for d in dados:
            c1, c2, c3, c4 = st.columns([1, 4, 1, 1])
            c1.write(d['os_n'])
            c2.write(d['cli'])
            
            # BOTÃO EDITAR (Lápis)
            if c3.button("✏️", key=f"ed_{d['ID']}"):
                st.session_state.edit_data = d
                navegar("📋 CADASTRO")
            
            # BOTÃO IMPRIMIR (PDF Completo)
            def gerar_pdf_os_completa(item):
                pdf = FPDF()
                pdf.add_page()
                
                # Cabeçalho Superior
                pdf.set_fill_color(0, 35, 102)
                pdf.rect(0, 0, 210, 40, 'F')
                pdf.set_text_color(255, 255, 255)
                pdf.set_font("Arial", 'B', 20)
                pdf.cell(190, 20, "ZION - ORDEM DE SERVICO", ln=True, align='C')
                
                pdf.ln(25)
                pdf.set_text_color(0, 0, 0)
                
                # --- BLOCO 1: DADOS GERAIS ---
                pdf.set_fill_color(230, 230, 230)
                pdf.set_font("Arial", 'B', 12)
                pdf.cell(190, 10, f" INFORMACOES GERAIS - O.S {item['os_n']}", 1, ln=True, fill=True)
                pdf.set_font("Arial", '', 10)
                
                # Organização das 17 colunas em blocos
                pdf.cell(95, 8, f"CLIENTE: {item['cli']}", 1)
                pdf.cell(95, 8, f"DATA SAIDA: {item['dt_s']}", 1, ln=True)
                pdf.cell(95, 8, f"EMPURRADOR: {item['emp']}", 1)
                pdf.cell(95, 8, f"BALSA: {item['bal']}", 1, ln=True)
                pdf.cell(95, 8, f"PEDIDO: {item['ped']}", 1)
                pdf.cell(95, 8, f"HORA EMBARQUE: {item['h_e']}", 1, ln=True)
                
                # --- BLOCO 2: OPERACIONAL ---
                pdf.set_font("Arial", 'B', 12)
                pdf.cell(190, 10, " DETALHES DA MISSAO", 1, ln=True, fill=True)
                pdf.set_font("Arial", '', 10)
                pdf.cell(95, 8, f"ORIGEM: {item['loc']}", 1)
                pdf.cell(95, 8, f"DESTINO: {item['dst']}", 1, ln=True)
                pdf.cell(95, 8, f"INICIO: {item['ini_m']}", 1)
                pdf.cell(95, 8, f"FIM: {item['fim_m']}", 1, ln=True)
                pdf.cell(95, 8, f"ESCOLTA 1: {item['esc1']}", 1)
                pdf.cell(95, 8, f"ESCOLTA 2: {item['esc2']}", 1, ln=True)
                pdf.cell(95, 8, f"MODALIDADE: {item.get('modalidade', 'ESCOLTA')}", 1)
                pdf.cell(95, 8, f"STATUS: {item['sts']}", 1, ln=True)
                
                # --- BLOCO 3: OBSERVAÇÕES ---
                pdf.ln(5)
                pdf.set_font("Arial", 'B', 10)
                pdf.cell(190, 8, "OBSERVACOES:", ln=True)
                pdf.set_font("Arial", '', 10)
                pdf.multi_cell(190, 7, f"{item['obs']}", 1)
                
                # --- BLOCO 4: ASSINATURAS (No rodapé) ---
                pdf.ln(25)
                # Linha para Solicitante
                pdf.line(20, pdf.get_y(), 90, pdf.get_y())
                # Linha para Prestador
                pdf.line(120, pdf.get_y(), 190, pdf.get_y())
                
                pdf.set_font("Arial", 'B', 8)
                pdf.cell(95, 5, "ASSINATURA DO SOLICITANTE", 0, 0, 'C')
                pdf.cell(95, 5, "ASSINATURA DO PRESTADOR (DIGITAL)", 0, 1, 'C')
                
                return pdf.output(dest='S').encode('latin-1')

            # Botão de Download PDF
            pdf_bytes = gerar_pdf_os_completa(d)
            c4.download_button("🖨️", pdf_bytes, f"OS_{d['os_n']}.pdf", "application/pdf", key=f"pr_btn_{d['ID']}")
            st.markdown("---")
   else:
            st.info("Nenhuma Ordem de Serviço registrada.")

# ATENÇÃO: O elif abaixo deve estar encostado na margem esquerda (sem espaços antes)
elif st.session_state.pagina == "💰 FINANCEIRO":
    st.markdown("<h1 style='text-align: center; color: white;'>💰 FINANCEIRO ESTRATÉGICO</h1>", unsafe_allow_html=True)
    if st.button("⬅️ VOLTAR PARA HOME"):
        navegar("🏠 HOME")
    
    dados = carregar_dados()
    if dados:
        df = pd.DataFrame(dados)
        st.write("### 📋 Lista de Operações")
        # Tabela simplificada para visualização rápida
        df_view_grade = df[['os_n', 'dt_s', 'cli', 'sts']].copy()
        df_view_grade.columns = ['Nº O.S', 'DATA SAÍDA', 'CLIENTE', 'STATUS']
        st.dataframe(df_view_grade, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        h1, h2, h3, h4 = st.columns([1, 4, 1, 1])
        h1.write("**O.S**")
        h2.write("**CLIENTE**")
        h3.write("**EDITAR**")
        h4.write("**PDF**")

        for d in dados:
            c1, c2, c3, c4 = st.columns([1, 4, 1, 1])
            c1.write(d['os_n'])
            c2.write(d['cli'])
            
            if c3.button("✏️", key=f"ed_{d['ID']}"):
                st.session_state.edit_data = d
                navegar("📋 CADASTRO")
            
            def gerar_pdf_os_total(item):
                pdf = FPDF()
                pdf.add_page()
                pdf.set_fill_color(0, 35, 102)
                pdf.rect(0, 0, 210, 40, 'F')
                pdf.set_text_color(255, 255, 255)
                pdf.set_font("Arial", 'B', 20)
                pdf.cell(190, 20, "ZION - ORDEM DE SERVICO", ln=True, align='C')
                pdf.ln(25); pdf.set_text_color(0, 0, 0)
                pdf.set_font("Arial", 'B', 12)
                pdf.cell(190, 10, f"DADOS COMPLETOS - O.S {item['os_n']}", border="B", ln=True)
                pdf.set_font("Arial", '', 10)
                
                # Campos detalhados para o PDF
                linhas = [
                    ("CLIENTE", item['cli']), ("DATA", item['dt_s']), 
                    ("ORIGEM", item['loc']), ("DESTINO", item['dst']),
                    ("EMPURRADOR", item['emp']), ("BALSA", item['bal']),
                    ("MODALIDADE", item.get('modalidade', 'ESCOLTA')), ("STATUS", item['sts'])
                ]
                for label, valor in linhas:
                    pdf.set_font("Arial", 'B', 10); pdf.cell(50, 8, f"{label}:", 0)
                    pdf.set_font("Arial", '', 10); pdf.cell(140, 8, f"{valor}", 0, ln=True)
                
                pdf.ln(20)
                pdf.line(20, pdf.get_y(), 90, pdf.get_y())
                pdf.line(120, pdf.get_y(), 190, pdf.get_y())
                pdf.set_font("Arial", 'B', 8)
                pdf.cell(95, 5, "ASSINATURA SOLICITANTE", 0, 0, 'C')
                pdf.cell(95, 5, "ASSINATURA PRESTADOR", 0, 1, 'C')
                return pdf.output(dest='S').encode('latin-1')

            c4.download_button("🖨️", gerar_pdf_os_total(d), f"OS_{d['os_n']}.pdf", key=f"pr_{d['ID']}")
            st.markdown("---")
    else:
        st.info("Nenhuma O.S registrada.")

# O BLOCO ABAIXO DEVE ESTAR EXATAMENTE ASSIM (NOVA LINHA E ALINHADO À ESQUERDA)
elif st.session_state.pagina == "💰 FINANCEIRO":
    st.markdown("<h1>💰 FINANCEIRO ESTRATÉGICO ZION</h1>", unsafe_allow_html=True)
    if st.button("⬅️ VOLTAR"): navegar("🏠 HOME")
    
    st.markdown("<style>[data-testid='stMetricValue'] {color: #ffff00 !important;}</style>", unsafe_allow_html=True)
    
    c_f1, c_f2, c_f3 = st.columns([1, 1, 2])
    data_ini = c_f1.date_input("Início", datetime.now(), format="DD/MM/YYYY")
    data_fim = c_f2.date_input("Fim", datetime.now(), format="DD/MM/YYYY")
    opcoes = ["Em Andamento", "Encerrado"]
    filtro_status = c_f3.multiselect("Status:", options=opcoes, default=opcoes)

    dados = carregar_dados()
    if dados:
        df = pd.DataFrame(dados)
        df['dt_s'] = pd.to_datetime(df['dt_s'], errors='coerce')
        df['ini_m'] = pd.to_datetime(df['ini_m'], errors='coerce')
        df['fim_m'] = pd.to_datetime(df['fim_m'], errors='coerce')

        def calc_fin(row):
            dias = (row['fim_m'] - row['ini_m']).days + 1 if pd.notnull(row['ini_m']) else 1
            serv = str(row.get('modalidade', 'ESCOLTA')).upper()
            v_unit = 970.0 if "VIGIL" in serv else 1870.0
            return pd.Series([dias, v_unit, dias * v_unit, "VIGILÂNCIA" if v_unit == 970 else "ESCOLTA"])

        df[['DIAS', 'V_UNIT', 'TOTAL_VAL', 'TIPO']] = df.apply(calc_fin, axis=1)
        
        mask = (df['dt_s'].dt.date >= data_ini) & (df['dt_s'].dt.date <= data_fim) & (df['sts'].isin(filtro_status))
        df_f = df.loc[mask].copy()

        if not df_f.empty:
            st.metric("Faturamento Total do Período", f"R$ {df_f['TOTAL_VAL'].sum():,.2f}")
            
            # Tabela com Origem, Destino e R$
            df_exibir = df_f.copy()
            df_exibir['TOTAL (R$)'] = df_exibir['TOTAL_VAL'].apply(lambda x: f"R$ {x:,.2f}")
            df_final = df_exibir[['os_n', 'cli', 'loc', 'dst', 'TIPO', 'DIAS', 'TOTAL (R$)', 'sts']]
            df_final.columns = ['Nº O.S', 'CLIENTE', 'ORIGEM', 'DESTINO', 'TIPO', 'DIAS', 'TOTAL (R$)', 'STATUS']
            st.dataframe(df_final, use_container_width=True, hide_index=True)

            def gerar_pdf_financeiro(df_rel, d1, d2):
                pdf = FPDF(orientation='L')
                pdf.add_page()
                pdf.set_fill_color(0, 35, 102)
                pdf.rect(0, 0, 297, 40, 'F')
                pdf.set_text_color(255, 255, 255)
                pdf.set_font("Arial", 'B', 18)
                pdf.cell(277, 15, "ZION TECNOLOGIA - RELATORIO FINANCEIRO", ln=True, align='C')
                pdf.ln(25); pdf.set_text_color(0, 0, 0); pdf.set_font("Arial", 'B', 8)
                
                # Cabeçalho PDF
                pdf.cell(20, 10, "O.S", 1, 0, 'C')
                pdf.cell(60, 10, "CLIENTE", 1, 0, 'C')
                pdf.cell(40, 10, "ORIGEM", 1, 0, 'C')
                pdf.cell(40, 10, "DESTINO", 1, 0, 'C')
                pdf.cell(30, 10, "TIPO", 1, 0, 'C')
                pdf.cell(40, 10, "TOTAL", 1, 1, 'C')
                
                pdf.set_font("Arial", '', 8)
                for _, r in df_rel.iterrows():
                    pdf.cell(20, 8, str(r['os_n']), 1, 0, 'C')
                    pdf.cell(60, 8, str(r['cli'])[:30], 1, 0, 'L')
                    pdf.cell(40, 8, str(r['loc'])[:20], 1, 0, 'L')
                    pdf.cell(40, 8, str(r['dst'])[:20], 1, 0, 'L')
                    pdf.cell(30, 8, str(r['TIPO']), 1, 0, 'C')
                    pdf.cell(40, 8, f"R$ {r['TOTAL_VAL']:,.2f}", 1, 1, 'R')
                return pdf.output(dest='S').encode('latin-1')

            st.download_button("🖨️ BAIXAR PDF FINANCEIRO", gerar_pdf_financeiro(df_f, data_ini, data_fim), "Financeiro_Zion.pdf")
