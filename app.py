import streamlit as st
import requests
import pandas as pd
import os
from datetime import datetime

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

# --- ESTILO CSS AZUL ROYAL ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(0, 35, 102, 0.9), rgba(0, 35, 102, 0.9)), 
                    url("https://images.unsplash.com/photo-1567899378494-47b22a2ae96a?q=80&w=2070&auto=format&fit=crop");
        background-size: cover; background-position: center; background-attachment: fixed;
    }
    h1, h2, h3, label { color: #00ff41 !important; text-shadow: 2px 2px 4px #000; text-align: center; }
    div.stButton > button:first-child[kind="primary"] { background-color: #28a745 !important; border: none; font-weight: bold; width: 100%; }
    .stDataFrame { background-color: rgba(15, 23, 42, 0.9); border: 1px solid #00ff41; border-radius: 10px; }
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
                
                # Tratamento flexível para o valor
                val = 0.0
                if "VALOR TOTAL" in p:
                    if p["VALOR TOTAL"]["type"] == "number":
                        val = p["VALOR TOTAL"]["number"] or 0.0
                    else:
                        txt_val = g_t("VALOR TOTAL").replace("R$", "").replace(".", "").replace(",", ".").strip()
                        try: val = float(txt_val)
                        except: val = 0.0

                lista.append({
                    "ID": r["id"],
                    "os_n": p["Nº OS"]["title"][0]["plain_text"] if p["Nº OS"]["title"] else "",
                    "cli": g_t("CLIENTE"), 
                    "dt_s": datetime.strptime(g_d("DT SAÍDA"), '%Y-%m-%d').date() if g_d("DT SAÍDA") else datetime.now().date(),
                    "dt_raw": g_d("DT SAÍDA"),
                    "emp": g_t("EMPURRADOR"), "bal": g_t("BALSA"), "ped": g_t("PEDIDO"),
                    "h_e": g_t("HORA DE EMBARQUE"), "esc1": g_t("ESCOLTA 1"), "esc2": g_t("ESCOLTA 2"),
                    "loc": g_t("LOCAL"), "dst": g_t("DESTINO"), "ass": g_t("ASSINATURA RESPONSÁVEL"),
                    "ini_m": g_d("INÍCIO DA MISSÃO"), "fim_m": g_d("FIM DA MISSÃO"),
                    "sts": status, "obs": g_t("DESCRIÇÃO"), "v_total": val
                })
            return lista
    except Exception as e:
        return []

# --- FUNÇÃO SALVAR NO NOTION (CORREÇÃO DE CONFLITO) ---
def salvar_no_notion(d, page_id=None):
    url = f"https://api.notion.com/v1/pages/{page_id}" if page_id else "https://api.notion.com/v1/pages"
    method = requests.patch if page_id else requests.post
    
    # Prepara o valor: remove pontos de milhar e troca vírgula por ponto
    try:
        valor_limpo = float(str(d['v_total']).replace("R$", "").replace(".", "").replace(",", ".").strip())
    except:
        valor_limpo = 0.0

    payload = {
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
            "ASSINATURA": {"rich_text": [{"text": {"content": str(d['ass'])}}]},
            "INÍCIO DA MISSÃO": {"date": {"start": d['ini_m'].strftime('%Y-%m-%d')}},
            "FIM DA MISSÃO": {"date": {"start": d['fim_m'].strftime('%Y-%m-%d')}},
            "STATUS": {"select": {"name": str(d['sts'])}},
            "DESCRIÇÃO": {"rich_text": [{"text": {"content": str(d['obs'])}}]},
            "VALOR TOTAL": {"number": valor_limpo}
        }
    }
    
    if not page_id: payload["parent"] = {"database_id": DATABASE}
    
    res = method(url, headers=headers, json=payload)
    return res.status_code in [200, 201, 202]

# --- NAVEGAÇÃO ---
if "pagina" not in st.session_state: st.session_state.pagina = "🏠 HOME"
if "edit_data" not in st.session_state: st.session_state.edit_data = None

def navegar(p):
    st.session_state.pagina = p
    st.rerun()

# --- TELAS ---
if st.session_state.pagina == "🏠 HOME":
    st.markdown("<h1>SISTEMA ZION</h1>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    if c1.button("📋 NOVO LANÇAMENTO"): 
        st.session_state.edit_data = None
        navegar("📋 CADASTRO")
    if c2.button("📊 VER AGENDAMENTOS"): navegar("📊 GRADE")
    if c3.button("💰 FINANCEIRO"): navegar("💰 FINANCEIRO")

elif st.session_state.pagina == "📋 CADASTRO":
    e = st.session_state.edit_data
    st.header("📋 EDIÇÃO" if e else "📋 NOVO REGISTRO")
    if st.button("⬅️ VOLTAR"): navegar("🏠 HOME")
    
    with st.form("form_os", clear_on_submit=False):
        c1, c2, c3 = st.columns(3)
        os_n = c1.text_input("Nº O.S", value=e['os_n'] if e else "")
        dt_s = c2.date_input("DATA SAÍDA", value=e['dt_s'] if e else datetime.now(), format="DD/MM/YYYY")
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
        loc = c10.text_input("LOCAL", value=e['loc'] if e else "")
        dst = c11.text_input("DESTINO", value=e['dst'] if e else "")
        ass = c12.text_input("ASSINATURA", value=e['ass'] if e else "")
        
        c13, c14, c15 = st.columns(3)
        ini_m = c13.date_input("INÍCIO MISSÃO", value=datetime.strptime(e['ini_m'], '%Y-%m-%d').date() if e and e['ini_m'] else datetime.now(), format="DD/MM/YYYY")
        fim_m = c14.date_input("FIM MISSÃO", value=datetime.strptime(e['fim_m'], '%Y-%m-%d').date() if e and e['fim_m'] else datetime.now(), format="DD/MM/YYYY")
        sts = c15.selectbox("STATUS", ["Em Andamento", "Encerrado"], index=0 if not e or e['sts'] == "Em Andamento" else 1)
        
        c16, c17 = st.columns([2, 1])
        obs = c16.text_area("DESCRIÇÃO", value=e['obs'] if e else "")
        v_total = c17.text_input("VALOR TOTAL", value=str(e['v_total']) if e else "0.00")

        if st.form_submit_button("✅ SALVAR OPERAÇÃO", type="primary"):
            dados_envio = {
                "os_n":os_n, "dt_s":dt_s, "cli":cli, "emp":emp, "bal":bal, "ped":ped, 
                "h_e":h_e, "esc1":esc1, "esc2":esc2, "loc":loc, "dst":dst, "ass":ass, 
                "ini_m":ini_m, "fim_m":fim_m, "sts":sts, "obs":obs, "v_total":v_total
            }
            if salvar_no_notion(dados_envio, e['ID'] if e else None):
                st.session_state.edit_data = None
                navegar("📊 GRADE")
            else:
                st.error("Erro ao salvar. Verifique se a coluna 'VALOR TOTAL' no Notion é do tipo NÚMERO.")

elif st.session_state.pagina == "📊 GRADE":
    st.header("📊 GRADE DE AGENDAMENTOS")
    if st.button("⬅️ VOLTAR"): navegar("🏠 HOME")
    dados = carregar_dados()
    
    cols_visualizacao = ["os_n", "cli", "dt_s", "sts"]
    if dados:
        df = pd.DataFrame(dados)
        st.dataframe(df[cols_visualizacao].rename(columns={"os_n":"OS", "cli":"CLIENTE", "dt_s":"DATA", "sts":"STATUS"}), use_container_width=True)
        for d in dados:
            with st.expander(f"⚙️ Gerenciar O.S {d['os_n']} - {d['cli']}"):
                if st.button(f"✏️ Editar", key=f"ed_{d['ID']}"):
                    st.session_state.edit_data = d
                    navegar("📋 CADASTRO")
    else:
        st.dataframe(pd.DataFrame(columns=cols_visualizacao), use_container_width=True)

elif st.session_state.pagina == "💰 FINANCEIRO":
    st.header("💰 RELATÓRIO FINANCEIRO")
    if st.button("⬅️ VOLTAR"): navegar("🏠 HOME")
    
    c1, c2 = st.columns(2)
    data_inicio = c1.date_input("De:", value=datetime.now().replace(day=1), format="DD/MM/YYYY")
    data_fim = c2.date_input("Até:", value=datetime.now(), format="DD/MM/YYYY")
    
    dados = carregar_dados()
    cols_fin = ["os_n", "cli", "dt_s", "v_total"]
    
    if dados:
        df = pd.DataFrame(dados)
        df['dt_conv'] = pd.to_datetime(df['dt_raw'])
        mask = (df['dt_conv'].dt.date >= data_inicio) & (df['dt_conv'].dt.date <= data_fim)
        df_filtrado = df.loc[mask]
        
        st.metric("FATURAMENTO NO PERÍODO", f"R$ {df_filtrado['v_total'].sum():,.2f}")
        st.dataframe(df_filtrado[cols_fin].rename(columns={"os_n":"OS", "cli":"CLIENTE", "dt_s":"DATA", "v_total":"VALOR"}), use_container_width=True)
    else:
        st.dataframe(pd.DataFrame(columns=cols_fin), use_container_width=True)
