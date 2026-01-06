import streamlit as st
import requests
import os
import pandas as pd

# Configuração da Página
st.set_page_config(page_title="Zion Tecnologia", layout="wide")

# Conexão Notion
TOKEN = st.secrets["notion"]["token"].replace('"', '').strip()
DATABASE = st.secrets["notion"]["database_id"].replace('"', '').strip()

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

# --- FUNÇÃO PARA BUSCAR DADOS DO NOTION ---
def buscar_dados():
    url = f"https://api.notion.com/v1/databases/{DATABASE}/query"
    res = requests.post(url, headers=headers)
    if res.status_code == 200:
        dados = res.json()["results"]
        lista = []
        for pg in dados:
            p = pg["properties"]
            # Extração segura de dados para a tabela
            lista.append({
                "Nº OS": p["Nº OS"]["title"][0]["text"]["content"] if p["Nº OS"]["title"] else "",
                "DATA INÍCIO": p["DATA INÍCIO"]["date"]["start"] if p["DATA INÍCIO"]["date"] else "",
                "CLIENTE": p["CLIENTE"]["rich_text"][0]["text"]["content"] if p["CLIENTE"]["rich_text"] else "",
                "ESCOLTA 1": p["ESCOLTA 1"]["rich_text"][0]["text"]["content"] if p["ESCOLTA 1"]["rich_text"] else "",
                "ESCOLTA 2": p["ESCOLTA 2"]["rich_text"][0]["text"]["content"] if p["ESCOLTA 2"]["rich_text"] else "",
                "STATUS": "FINALIZADO" # Exemplo de status fixo como no vídeo
            })
        return pd.DataFrame(lista)
    return pd.DataFrame()

# --- ESTADO DE NAVEGAÇÃO ---
if "pagina" not in st.session_state:
    st.session_state.pagina = "🏠 HOME"

# --- BARRA LATERAL ---
with st.sidebar:
    if os.path.exists("LOGO.PNG"):
        if st.button("🏠 VOLTAR À CENTRAL", use_container_width=True):
            st.session_state.pagina = "🏠 HOME"
            st.rerun()
        st.image("LOGO.PNG", use_container_width=True)
    
    st.markdown("---")
    menu_opcoes = ["🏠 HOME", "📋 AGENDAMENTO ZION", "📊 VER AGENDAMENTOS", "💰 FINANCEIRO", "🖨️ GERAR PDF"]
    st.session_state.pagina = st.radio("NAVEGAÇÃO", menu_opcoes, index=menu_opcoes.index(st.session_state.pagina))

# --- TELA 1: HOME ---
if st.session_state.pagina == "🏠 HOME":
    st.title("🛡️ Zion Tecnologia - Central de Gestão")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📋 NOVO AGENDAMENTO", use_container_width=True):
            st.session_state.pagina = "📋 AGENDAMENTO ZION"; st.rerun()
    with col2:
        if st.button("📊 VER REGISTROS", use_container_width=True):
            st.session_state.pagina = "📊 VER AGENDAMENTOS"; st.rerun()
    with col3:
        if st.button("💰 FINANCEIRO", use_container_width=True):
            st.session_state.pagina = "💰 FINANCEIRO"; st.rerun()
    st.image("LOGO.PNG", width=400)

# --- TELA 2: AGENDAMENTO (SALVAMENTO CORRIGIDO) ---
elif st.session_state.pagina == "📋 AGENDAMENTO ZION":
    st.header("📋 Cadastro de Operação")
    with st.form("form_zion", clear_on_submit=True):
        c1, c2, c3 = st.columns(3)
        os_n = c1.text_input("Nº OS")
        data_ini = c2.date_input("DATA INÍCIO", format="DD/MM/YYYY")
        data_fim = c3.date_input("DATA FIM", format="DD/MM/YYYY")
        
        c4, c5, c6 = st.columns(3)
        esc1 = c4.text_input("ESCOLTA 1")
        esc2 = c5.text_input("ESCOLTA 2")
        hora_emb = c6.text_input("HORA EMBARQUE")
        
        c7, c8, c9 = st.columns(3)
        local = c7.text_input("LOCAL")
        empurrador = c8.text_input("EMPURRADOR")
        saida = c9.text_input("SAÍDA")
        
        cliente = st.text_input("CLIENTE")
        desc = st.text_area("DESCRIÇÃO")

        if st.form_submit_button("✅ SALVAR OPERAÇÃO"):
            payload = {
                "parent": {"database_id": DATABASE},
                "properties": {
                    "Nº OS": {"title": [{"text": {"content": os_n}}]},
                    "CLIENTE": {"rich_text": [{"text": {"content": cliente}}]},
                    "DATA INÍCIO": {"date": {"start": str(data_ini)}},
                    "DATA FIM": {"date": {"start": str(data_fim)}},
                    "ESCOLTA 1": {"rich_text": [{"text": {"content": esc1}}]},
                    "ESCOLTA 2": {"rich_text": [{"text": {"content": esc2}}]},
                    "HORA EMBARQUE": {"rich_text": [{"text": {"content": hora_emb}}]},
                    "LOCAL": {"rich_text": [{"text": {"content": local}}]},
                    "EMPURRADOR": {"rich_text": [{"text": {"content": empurrador}}]},
                    "SAÍDA": {"rich_text": [{"text": {"content": saida}}]},
                    "DESCRIÇÃO": {"rich_text": [{"text": {"content": desc}}]}
                }
            }
            res = requests.post("https://api.notion.com/v1/pages", headers=headers, json=payload)
            if res.status_code == 200:
                st.success("🎯 AGORA FOI! Verifique sua tabela.")
            else:
                st.error(f"Erro: {res.text}")

# --- TELA 3: CONSULTA (A TELA QUE FALTAVA) ---
elif st.session_state.pagina == "📊 VER AGENDAMENTOS":
    st.header("📊 Operações Realizadas")
    df = buscar_dados()
    if not df.empty:
        # Mostra a tabela igual ao vídeo
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("Nenhum registro encontrado.")
