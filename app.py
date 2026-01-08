import streamlit as st
import pandas as pd
from datetime import datetime

# 1. CONFIGURAÇÃO DE TELA (Mobile-First)
st.set_page_config(page_title="Zion Tecnologia", layout="wide", initial_sidebar_state="collapsed")

# 2. MOTOR DE NAVEGAÇÃO
if 'pagina' not in st.session_state:
    st.session_state.pagina = "🏠 HOME"

def navegar(destino):
    st.session_state.pagina = destino
    st.rerun()

# 3. ESTILO VISUAL (Azul Suave e Limpeza de Erros)
st.markdown("""
<style>
    /* Azul Suave e Profundo */
    .stApp {
        background: linear-gradient(135deg, #001233 0%, #002855 100%) !important;
    }
    
    /* Remove as faixas de erro padrão do Streamlit que poluem o visual */
    .stAlert { display: none !important; }

    /* Estilo dos Botões */
    div.stButton > button {
        width: 100%;
        height: 100px !important;
        background: rgba(255, 255, 255, 0.05) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 15px !important;
        font-weight: bold !important;
    }
    
    div.stButton > button:hover {
        border-color: #00ff41 !important;
        background: rgba(255, 255, 255, 0.1) !important;
    }

    .icon-wrapper {
        text-align: center;
        margin-bottom: -15px;
    }
    
    h1 { color: white !important; text-align: center; font-size: 28px !important; }
</style>
""", unsafe_allow_html=True)

# --- FUNÇÃO CARREGAR DADOS ---
def carregar_dados():
    try:
        res = requests.post(f"https://api.notion.com/v1/databases/{DATABASE}/query", headers=headers)
        if res.status_code == 200:
            results = res.json().get("results", [])
            lista = []
            for r in results:
                p = r["properties"]
                def g_t(n): 
                    try: return p[n]["rich_text"][0]["plain_text"] if p[n]["rich_text"] else ""
                    except: return ""
                def g_d(n): 
                    try: return p[n]["date"]["start"] if p[n]["date"] else None
                    except: return None
                
                status = p["STATUS"]["select"]["name"] if "STATUS" in p and p["STATUS"]["select"] else "Em Andamento"
                valor_os = 0.0
                try: valor_os = p["VALOR TOTAL"]["number"] if p["VALOR TOTAL"]["number"] else 0.0
                except: valor_os = 0.0

                lista.append({
                    "ID": r["id"],
                    "Nº OS": p["Nº OS"]["title"][0]["plain_text"] if p["Nº OS"]["title"] else "---",
                    "CLIENTE": g_t("CLIENTE"), 
                    "DT SAÍDA": datetime.strptime(g_d("DT SAÍDA"), '%Y-%m-%d').strftime('%d/%m/%Y') if g_d("DT SAÍDA") else "---",
                    "DT_RAW": g_d("DT SAÍDA"),
                    "EMPURRADOR": g_t("EMPURRADOR"), "BALSA": g_t("BALSA"),
                    "PEDIDO": g_t("PEDIDO"), "HORA_EMBARQUE": g_t("HORA DE EMBARQUE"),
                    "ESCOLTA 1": g_t("ESCOLTA 1"), "ESCOLTA 2": g_t("ESCOLTA 2"),
                    "LOCAL": g_t("LOCAL"), "DESTINO": g_t("DESTINO"),
                    "ASSINATURA": g_t("ASSINATURA RESPONSÁVEL"),
                    "STATUS": status, "VALOR": valor_os
                })
            return lista
    except: return []

# --- FUNÇÃO SALVAR NO NOTION (17 COLUNAS) ---
def salvar_no_notion(d):
    url = "https://api.notion.com/v1/pages"
    payload = {
        "parent": {"database_id": DATABASE},
        "properties": {
            "Nº OS": {"title": [{"text": {"content": str(d['os_n'])}}]},
            "CLIENTE": {"rich_text": [{"text": {"content": str(d['cli'])}}]},
            "DT SAÍDA": {"date": {"start": d['dt_s'].strftime('%Y-%m-%d')}},
            "EMPURRADOR": {"rich_text": [{"text": {"content": str(d['emp'])}}]},
            "BALSA": {"rich_text": [{"text": {"content": str(d['bal'])}}]},
            "PEDIDO": {"rich_text": [{"text": {"content": str(d['ped'])}}]},
            "HORA DE EMBARQUE": {"rich_text": [{"text": {"content": str(d['h_e'])}}]},
            "ESCOLTA 1": {"rich_text": [{"text": {"content": str(d['esc1'])}}]},
            "ESCOLTA 2": {"rich_text": [{"text": {"content": str(d['esc2'])}}]},
            "LOCAL": {"rich_text": [{"text": {"content": str(d['loc'])}}]},
            "DESTINO": {"rich_text": [{"text": {"content": str(d['dst'])}}]},
            "ASSINATURA RESPONSÁVEL": {"rich_text": [{"text": {"content": str(d['ass'])}}]},
            "INÍCIO DA MISSÃO": {"date": {"start": d['ini_m'].strftime('%Y-%m-%d')}},
            "FIM DA MISSÃO": {"date": {"start": d['fim_m'].strftime('%Y-%m-%d')}},
            "STATUS": {"select": {"name": str(d['sts'])}},
            "DESCRIÇÃO": {"rich_text": [{"text": {"content": str(d['obs'])}}]},
            "VALOR TOTAL": {"number": float(d['v_total']) if d['v_total'] else 0.0}
        }
    }
    res = requests.post(url, headers=headers, json=payload)
    return res.status_code == 200

# --- NAVEGAÇÃO ---
if "pagina" not in st.session_state: st.session_state.pagina = "🏠 HOME"
def navegar(p): st.session_state.pagina = p; st.rerun()

#---- Tela Inicial ----# 
if st.session_state.pagina == "🏠 HOME":
    st.markdown("<h1>ZION BUSINESS</h1>", unsafe_allow_html=True)
    st.markdown("<div style='margin-bottom: 50px;'></div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        # Ícone acima do botão
        st.markdown('<div class="icon-wrapper"><img src="https://cdn-icons-png.flaticon.com/512/6819/6819643.png" width="70"></div>', unsafe_allow_html=True)
        if st.button("📝 CADASTRO", key="btn_cad"):
            navegar("📋 CADASTRO")

    with col2:
        # Ícone acima do botão
        st.markdown('<div class="icon-wrapper"><img src="https://cdn-icons-png.flaticon.com/512/2693/2693507.png" width="70"></div>', unsafe_allow_html=True)
        if st.button("📅 OPERACIONAL", key="btn_grade"):
            navegar("📊 GRADE")

    with col3:
        # Ícone acima do botão
        st.markdown('<div class="icon-wrapper"><img src="https://cdn-icons-png.flaticon.com/512/10543/10543111.png" width="70"></div>', unsafe_allow_html=True)
        if st.button("💰 FINANCEIRO", key="btn_fin"):
            navegar("💰 FINANCEIRO")

    # A logo e a faixa vermelha foram removidas daqui para limpar o visual.
    # Logo Footer
    st.markdown(f"""
        <div style="text-align: center; margin-top: 50px; padding: 20px;">
            <img src="data:image/png;base64,{img_base64}" style="width: 200px; opacity: 0.8; filter: drop-shadow(0px 5px 15px rgba(0,0,0,0.5));">
            <p style="color: rgba(255,255,255,0.5) !important; font-size: 12px; margin-top: 10px;">
                ZION TECNOLOGIA © 2026
            </p>
        </div>
    """, unsafe_allow_html=True)

    # --- CÓDIGO PARA CARREGAR IMAGEM DA BIBLIOTECA LOCAL ---
    try:
        # Substitua 'logo.png' pelo nome exato do arquivo que está na sua pasta
        nome_arquivo_logo = "logo.png" 
        
        with open(nome_arquivo_logo, "rb") as f:
            data = base64.b64encode(f.read()).decode("utf-8")
            
        st.markdown(f"""
            <div class="logo-footer">
                <img src="data:image/png;base64,{data}" class="logo-img">
            </div>
        """, unsafe_allow_html=True)
    except FileNotFoundError:
        st.error("⚠️ Erro: O arquivo da logo não foi encontrado na pasta do sistema.")
#---- Tela Cadastro ----# 
elif st.session_state.pagina == "📋 CADASTRO":
    st.header("📋 NOVO REGISTRO (17 COLUNAS)")
    if st.button("⬅️ VOLTAR"): navegar("🏠 HOME")
    with st.form("form_os"):
        c1, c2, c3 = st.columns(3)
        os_n, dt_s, cli = c1.text_input("Nº O.S"), c2.date_input("DATA SAÍDA", format="DD/MM/YYYY"), c3.text_input("CLIENTE")
        c4, c5, c6 = st.columns(3)
        emp, bal, ped = c4.text_input("EMPURRADOR"), c5.text_input("BALSA"), c6.text_input("PEDIDO")
        c7, c8, c9 = st.columns(3)
        h_e, esc1, esc2 = c7.text_input("HORA EMBARQUE"), c8.text_input("ESCOLTA 1"), c9.text_input("ESCOLTA 2")
        c10, c11, c12 = st.columns(3)
        loc, dst, ass = c10.text_input("LOCAL"), c11.text_input("DESTINO"), c12.text_input("ASSINATURA RESP.")
        c13, c14, c15 = st.columns(3)
        ini_m, fim_m, sts = c13.date_input("INÍCIO MISSÃO", format="DD/MM/YYYY"), c14.date_input("FIM MISSÃO", format="DD/MM/YYYY"), c15.selectbox("STATUS", ["Em Andamento", "Encerrado"])
        c16, c17 = st.columns([2, 1])
        obs, v_total = c16.text_area("DESCRIÇÃO"), c17.text_input("VALOR TOTAL", value="0.0")
        
        if st.form_submit_button("✅ SALVAR OPERAÇÃO", type="primary"):
            d = {"os_n":os_n, "dt_s":dt_s, "cli":cli, "emp":emp, "bal":bal, "ped":ped, "h_e":h_e, "esc1":esc1, "esc2":esc2, "loc":loc, "dst":dst, "ass":ass, "ini_m":ini_m, "fim_m":fim_m, "sts":sts, "obs":obs, "v_total":v_total}
            if salvar_no_notion(d): navegar("📊 GRADE")
            else: st.error("Erro ao salvar no Notion.")

#---- Tela Grade ----# 
elif st.session_state.pagina == "📊 GRADE":
    st.markdown("<h1>📊 GRADE DE OPERAÇÕES</h1>", unsafe_allow_html=True)
    if st.button("⬅️ VOLTAR"):
        navegar("🏠 HOME")

    # Exemplo de loop de dados corrigido
    dados = carregar_dados() # Sua função do Notion
    if dados:
        for d in dados:
            st.write(f"**OS:** {d.get('os_n')} | **Cliente:** {d.get('cli')}")
            # Alinhamento exato para evitar erro
            st.markdown("---") 
    else:
        st.info("Nenhum registro encontrado.")
#---- Tela Financeiro ----# 
elif st.session_state.pagina == "💰 FINANCEIRO":
    st.markdown("<h1>💰 PAINEL FINANCEIRO</h1>", unsafe_allow_html=True)
    if st.button("⬅️ VOLTAR"):
        navegar("🏠 HOME")
    
    # Adicione suas métricas aqui
    st.metric("Faturamento Total", "R$ 0,00", "+5%")
    st.write("Detalhamento de custos e lucros...")
