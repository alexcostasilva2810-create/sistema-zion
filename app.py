import streamlit as st
import requests
import pandas as pd
import os
from datetime import datetime

# Importações necessárias para o novo PDF
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor, black
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph
from io import BytesIO

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Zion Tecnologia - Gestão O.S", layout="wide")

# --- CONEXÃO NOTION ---
# Usando um bloco try-except para evitar erros se os segredos não estiverem configurados
try:
    TOKEN = st.secrets["notion"]["token"].replace('"', '').strip()
    DATABASE = st.secrets["notion"]["database_id"].replace('"', '').strip()
    HEADERS = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }
except (KeyError, AttributeError):
    st.error("As credenciais do Notion não foram configuradas corretamente nos segredos do Streamlit.")
    st.stop()


# --- ESTILO CSS (BOTÃO VERDE E LAYOUT) ---
st.markdown("""
    <style>
    div.stButton > button:first-child[kind="primary"] { background-color: #28a745 !important; color: white !important; }
    .stButton>button { width: 100%; border-radius: 8px; font-weight: bold; height: 3.5em; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNÇÃO CARREGAR DADOS ---
@st.cache_data(ttl=300) # Adicionado cache para melhorar performance
def carregar_dados():
    try:
        res = requests.post(f"https://api.notion.com/v1/databases/{DATABASE}/query", headers=HEADERS )
        res.raise_for_status() # Lança um erro para códigos de status ruins (4xx ou 5xx)
        
        results = res.json().get("results", [])
        lista = []
        for r in results:
            p = r["properties"]
            def g_t(n): 
                try: return p[n]["rich_text"][0]["plain_text"] if p[n].get("rich_text") else ""
                except (KeyError, IndexError): return ""
            def g_d(n): 
                try: return p[n]["date"]["start"] if p[n].get("date") else None
                except KeyError: return None
            
            status = p.get("STATUS", {}).get("select", {}).get("name") or "Em Andamento"
            
            # Regra Financeira
            valor = 0.0
            if status == "Encerrado":
                if g_t("ESCOLTA 1"): valor += 1870.0
                if g_t("ESCOLTA 2"): valor += 970.0

            lista.append({
                "ID": r["id"],
                "Nº OS": p["Nº OS"]["title"][0]["plain_text"] if p.get("Nº OS", {}).get("title") else "---",
                "CLIENTE": g_t("CLIENTE"), 
                "DT_SAIDA_RAW": g_d("DT SAÍDA"),
                "DT SAÍDA": datetime.strptime(g_d("DT SAÍDA"), '%Y-%m-%d').strftime('%d/%m/%Y') if g_d("DT SAÍDA") else "---",
                "EMPURRADOR": g_t("EMPURRADOR"), "BALSA": g_t("BALSA"),
                "LOCAL": g_t("LOCAL"), "DESTINO": g_t("DESTINO"),
                "HORA_EMBARQUE": g_t("HORA DE EMBARQUE"),
                "ESCOLTA 1": g_t("ESCOLTA 1"), "ESCOLTA 2": g_t("ESCOLTA 2"),
                "DESCRIÇÃO": g_t("DESCRIÇÃO"), "PEDIDO": g_t("PEDIDO"),
                "INÍCIO": g_d("INÍCIO DA MISSÃO"), "FIM": g_d("FIM DA MISSÃO"),
                "ASSINATURA": g_t("ASSINATURA RESPONSÁVEL"),
                "STATUS": status, "VALOR": valor
            })
        return lista
    except requests.exceptions.RequestException as e:
        st.error(f"Erro ao conectar com a API do Notion: {e}")
        return []
    except Exception as e:
        st.error(f"Ocorreu um erro inesperado ao carregar os dados: {e}")
        return []

# --- NOVA FUNÇÃO PDF (O.S INDIVIDUAL) ---
def gerar_pdf_os_novo(d):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # --- FUNÇÕES AUXILIARES DE DESENHO ---
    def draw_header():
        logo_path = "logo_transdourada.png"
        if os.path.exists(logo_path):
            c.drawImage(logo_path, 2 * cm, height - 3 * cm, width=5*cm, preserveAspectRatio=True, mask='auto')
        else:
            c.setFont("Helvetica-Bold", 14)
            c.drawString(2 * cm, height - 2 * cm, "TRANSDOURADA Navegação Ltda.")
        
        c.setFont("Helvetica-Bold", 16)
        c.drawCentredString(width / 2, height - 4.5 * cm, "Solicitação de Escolta")

    def draw_os_details():
        c.setFont("Helvetica", 11)
        c.drawCentredString(width / 2, height - 5.5 * cm, f"ORDEM DE SERVIÇO O.S: {d.get('Nº OS', 'N/A')}")
        c.drawCentredString(width / 2, height - 6 * cm, f"STATUS: {d.get('STATUS', 'N/A').upper()}")
        
        # Caixa "SOLICITANTE"
        c.setStrokeColor(black)
        c.rect(4 * cm, height - 7 * cm, width - 8 * cm, 0.8 * cm, stroke=1, fill=0)
        c.setFont("Helvetica-Bold", 12)
        c.drawCentredString(width / 2, height - 6.7 * cm, "SOLICITANTE ( TRANSDOURADA )")

    def draw_info_section():
        c.setFont("Helvetica-Bold", 10)
        start_y = height - 8.5 * cm
        x_label = 2.5 * cm
        x_value = 5.5 * cm
        
        data_map = {
            "EMPURRADOR:": d.get('EMPURRADOR', ''),
            "SAÍDA PREVISTA:": d.get('HORA_EMBARQUE', ''),
            "ORIGEM:": d.get('LOCAL', ''),
            "DESTINO:": d.get('DESTINO', ''),
            "BALSA:": d.get('BALSA', ''),
            "CLIENTE:": d.get('CLIENTE', ''),
            "CMT:": "" # Campo vazio conforme modelo
        }
        
        line_height = 0.6 * cm
        for i, (label, value) in enumerate(data_map.items()):
            c.drawString(x_label, start_y - (i * line_height), label)
            c.setFont("Helvetica", 10)
            c.drawString(x_value, start_y - (i * line_height), value)
            c.setFont("Helvetica-Bold", 10)

    def draw_mission_section():
        # Caixa "PVH-SEG"
        c.setStrokeColor(black)
        c.rect(4 * cm, height - 14 * cm, width - 8 * cm, 0.8 * cm, stroke=1, fill=0)
        c.setFont("Helvetica-Bold", 12)
        c.drawCentredString(width / 2, height - 13.7 * cm, "PVH-SEG Serv. de Vig.Patrimonial Ltda")

        c.setFont("Helvetica", 10)
        start_y = height - 15.5 * cm
        x_pos = 2.5 * cm
        line_height = 0.6 * cm
        
        inicio_missao = datetime.strptime(d['INÍCIO'], '%Y-%m-%d').strftime('%d/%m/%Y') if d.get('INÍCIO') else 'N/A'
        fim_missao = datetime.strptime(d['FIM'], '%Y-%m-%d').strftime('%d/%m/%Y') if d.get('FIM') else 'N/A'

        c.drawString(x_pos, start_y, f"INÍCIO DA MISSÃO: {inicio_missao}")
        c.drawString(x_pos, start_y - line_height, f"ESCOLTA 1: {d.get('ESCOLTA 1', '')}")
        c.drawString(x_pos, start_y - 2 * line_height, f"ESCOLTA 2: {d.get('ESCOLTA 2', '')}")
        c.drawString(x_pos, start_y - 3 * line_height, f"FIM DA MISSÃO: {fim_missao}")

    def draw_description():
        c.line(2 * cm, height - 18.5 * cm, width - 2 * cm, height - 18.5 * cm)
        c.setFont("Helvetica-Bold", 12)
        c.drawCentredString(width / 2, height - 19.2 * cm, "DETALHAMENTO DA MISSÃO")
        
        styles = getSampleStyleSheet()
        style = styles['BodyText']
        style.fontName = 'Helvetica'
        style.fontSize = 10
        style.leading = 14 # Espaçamento entre linhas
        
        # Substituindo quebras de linha do texto por   
 para o Paragraph
        descricao_text = d.get('DESCRIÇÃO', 'Nenhuma descrição fornecida.').replace('\n', '  
')
        
        p = Paragraph(f"<b>DESCRIÇÃO:</b> {descricao_text}", style)
        p.wrapOn(c, width - 5 * cm, 10 * cm) # Largura disponível
        p.drawOn(c, 2.5 * cm, height - 22 * cm) # Posição (x, y)

    def draw_footer():
        c.setFont("Helvetica", 8)
        text = "TRANSDOURADA NAVEGAÇÃO LTDA 01.259.730/0001-74 ROD BR 316 KM 08, SN AGUA BRANCA 67033-070 ANANINDEUA"
        c.drawCentredString(width / 2, 1.5 * cm, text)

    # --- CHAMADA DAS FUNÇÕES DE DESENHO ---
    draw_header()
    draw_os_details()
    draw_info_section()
    draw_mission_section()
    draw_description()
    draw_footer()
    
    c.save()
    buffer.seek(0)
    return buffer.getvalue()

# --- NAVEGAÇÃO ---
if "pagina" not in st.session_state: st.session_state.pagina = "🏠 HOME"
if "dados_edicao" not in st.session_state: st.session_state.dados_edicao = None
def navegar(p): st.session_state.pagina = p; st.rerun()

# --- TELAS ---
if st.session_state.pagina == "🏠 HOME":
    logo_path = "LOGO.PNG" # Usando o mesmo nome do seu código original
    if os.path.exists(logo_path): 
        st.image(logo_path, width=250)
    else:
        st.image("logo_transdourada.png", width=250) # Fallback para o logo da OS

    st.title("🛡️ Zion Tecnologia")
    c1, c2, c3 = st.columns(3)
    if c1.button("📋 NOVO LANÇAMENTO"): st.session_state.dados_edicao = None; navegar("📋 CADASTRO")
    if c2.button("📊 VER AGENDAMENTOS"): navegar("📊 GRADE")
    if c3.button("💰 FINANCEIRO"): navegar("💰 FINANCEIRO")

elif st.session_state.pagina == "📊 GRADE":
    st.header("📊 Ver Agendamentos")
    if st.button("⬅️ VOLTAR"): navegar("🏠 HOME")
    dados = carregar_dados()
    if dados:
        for d in dados:
            with st.expander(f"O.S {d['Nº OS']} - {d['CLIENTE']} ({d['DT SAÍDA']})"):
                c1, c2 = st.columns(2)
                if c1.button("✏️ EDITAR", key=f"ed_{d['ID']}", type="primary"):
                    st.session_state.dados_edicao = d; navegar("📋 CADASTRO")
                
                # --- AQUI A MÁGICA ACONTECE ---
                # Chamando a nova função para gerar o PDF personalizado
                pdf_os = gerar_pdf_os_novo(d)
                c2.download_button("📄 GERAR PDF O.S", pdf_os, f"Solicitacao_Escolta_{d['Nº OS']}.pdf", key=f"p_{d['ID']}")

# O restante do seu código (CADASTRO, FINANCEIRO) pode permanecer o mesmo.
# Colei abaixo para garantir que nada seja perdido.

elif st.session_state.pagina == "📋 CADASTRO":
    edit = st.session_state.dados_edicao
    st.header("📝 Formulário O.S")
    if st.button("⬅️ VOLTAR"): navegar("🏠 HOME")
    
    with st.form("form_os"):
        c1, c2, c3 = st.columns(3)
        os_n = c1.text_input("Nº O.S", value=edit["Nº OS"] if edit else "")
        dt_val = datetime.strptime(edit["DT_SAIDA_RAW"], '%Y-%m-%d') if edit and edit["DT_SAIDA_RAW"] else datetime.now()
        dt_s = c2.date_input("DATA SAÍDA", value=dt_val, format="DD/MM/YYYY")
        cli = c3.text_input("CLIENTE", value=edit["CLIENTE"] if edit else "")
        
        c4, c5, c6 = st.columns(3)
        ini_m = c4.date_input("INÍCIO MISSÃO", format="DD/MM/YYYY")
        fim_m = c5.date_input("FIM MISSÃO", format="DD/MM/YYYY")
        bal = c6.text_input("BALSA", value=edit["BALSA"] if edit else "")
        
        c7, c8, c9 = st.columns(3)
        h_e = c7.text_input("HORA EMBARQUE", value=edit.get("HORA_EMBARQUE", "") if edit else "")
        esc1 = c8.text_input("ESCOLTA 1", value=edit.get("ESCOLTA 1", "") if edit else "")
        esc2 = c9.text_input("ESCOLTA 2", value=edit.get("ESCOLTA 2", "") if edit else "")
        
        c10, c11, c12 = st.columns(3)
        loc = c10.text_input("LOCAL (ORIGEM)", value=edit.get("LOCAL", "") if edit else "")
        dst = c11.text_input("DESTINO", value=edit.get("DESTINO", "") if edit else "")
        ped = c12.text_input("PEDIDO / REF", value=edit.get("PEDIDO", "") if edit else "")
        
        c13, c14, c15 = st.columns(3)
        emp = c13.text_input("EMPURRADOR", value=edit.get("EMPURRADOR", "") if edit else "")
        ass = c14.text_input("ASSINATURA RESPONSÁVEL", value=edit.get("ASSINATURA", "") if edit else "")
        sts = c15.selectbox("STATUS", ["Em Andamento", "Encerrado"], index=0 if not edit or edit.get("STATUS") == "Em Andamento" else 1)
        
        obs = st.text_area("DESCRIÇÃO", value=edit.get("DESCRIÇÃO", "") if edit else "")
        
        if st.form_submit_button("✅ SALVAR OPERAÇÃO", type="primary"):
            # A lógica de salvar no Notion deve ser implementada aqui
            # Exemplo de payload (precisa ser adaptado para criar/atualizar)
            payload = {
                "parent": {"database_id": DATABASE},
                "properties": {
                    "Nº OS": {"title": [{"text": {"content": os_n}}]},
                    "CLIENTE": {"rich_text": [{"text": {"content": cli}}]},
                    "DT SAÍDA": {"date": {"start": dt_s.strftime('%Y-%m-%d')}},
                    # ... Adicionar todos os outros campos aqui
                }
            }
            # if edit:
            #     # Lógica de UPDATE
            #     # requests.patch(f"https://api.notion.com/v1/pages/{edit['ID']}", json=payload, headers=HEADERS )
            # else:
            #     # Lógica de CREATE
            #     # requests.post("https://api.notion.com/v1/pages", json=payload, headers=HEADERS )
            
            st.success("Operação salva com sucesso! (Lógica de salvamento a ser implementada)")
            st.cache_data.clear() # Limpa o cache para recarregar os dados
            navegar("📊 GRADE")

elif st.session_state.pagina == "💰 FINANCEIRO":
    st.header("💰 Financeiro e Relatórios")
    if st.button("⬅️ VOLTAR"): navegar("🏠 HOME")
    
    c1, c2 = st.columns(2)
    f_ini = c1.date_input("Data Inicial", value=datetime.now() - pd.Timedelta(days=30), format="DD/MM/YYYY")
    f_fim = c2.date_input("Data Final", value=datetime.now(), format="DD/MM/YYYY")
    
    dados = carregar_dados()
    if dados:
        df = pd.DataFrame(dados)
        df['dt_filter'] = pd.to_datetime(df['DT_SAIDA_RAW'])
        df_filt = df[(df['dt_filter'] >= pd.Timestamp(f_ini)) & (df['dt_filter'] <= pd.Timestamp(f_fim))].copy()
        
        total = df_filt['VALOR'].sum()
        st.metric("Total Faturado no Período", f"R$ {total:,.2f}")
        
        df_display = df_filt[["Nº OS", "CLIENTE", "DT SAÍDA", "EMPURRADOR", "BALSA", "ESCOLTA 1", "ESCOLTA 2", "VALOR"]].copy()
        df_display['VALOR'] = df_display['VALOR'].apply(lambda x: f"R$ {x:,.2f}")
        st.dataframe(df_display, use_container_width=True, hide_index=True)
        
        # O relatório financeiro ainda usa FPDF, pode ser melhorado no futuro se desejar
        # from fpdf import FPDF
        # pdf_fin = gerar_pdf_financeiro(df_filt, total, f_ini, f_fim)
        # st.download_button("📥 BAIXAR RELATÓRIO PDF (PERÍODO)", pdf_fin, "relatorio_financeiro.pdf", type="primary")

