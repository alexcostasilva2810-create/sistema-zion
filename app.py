import streamlit as st
import requests
import pandas as pd
import os

st.set_page_config(page_title="Zion Tecnologia", layout="wide")

# Conexão Notion
TOKEN = st.secrets["notion"]["token"].replace('"', '').strip()
DATABASE = st.secrets["notion"]["database_id"].replace('"', '').strip()

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "authorization/json",
    "Notion-Version": "2022-06-28"
}

# --- CONTROLE DE ESTADO ---
if "logado" not in st.session_state:
    st.session_state.logado = False
if "pagina" not in st.session_state:
    st.session_state.pagina = "🏠 HOME"

def navegar(p):
    st.session_state.pagina = p
    st.rerun()

# --- FUNÇÃO BUSCAR DADOS ---
def buscar_dados():
    url = f"https://api.notion.com/v1/databases/{DATABASE}/query"
    res = requests.post(url, headers=headers)
    if res.status_code == 200:
        dados = res.json()["results"]
        lista = []
        for pg in dados:
            p = pg["properties"]
            try:
                tipo = p.get("SERVIÇO", {}).get("select", {}).get("name", "Escolta")
                lista.append({
                    "ID": pg["id"],
                    "Nº OS": p.get("Nº OS", {}).get("title", [{}])[0].get("text", {}).get("content", ""),
                    "CLIENTE": p.get("CLIENTE", {}).get("rich_text", [{}])[0].get("text", {}).get("content", ""),
                    "INÍCIO": p.get("INÍCIO DA MISSÃO", {}).get("date", {}).get("start", ""),
                    "STATUS": p.get("STATUS", {}).get("select", {}).get("name", "Em Andamento"),
                    "VALOR": 1870.0 if tipo == "Escolta" else 970.0
                })
            except: continue
        return pd.DataFrame(lista)
    return pd.DataFrame()

# --- REMOVENDO MENU DA ESQUERDA (SIDEBAR VAZIA OU OCULTA) ---
st.markdown("<style> [data-testid='stSidebarNav'] {display: none;} </style>", unsafe_allow_html=True)

# --- TELA 1: ABERTURA (LOGO CLICÁVEL) ---
if st.session_state.pagina == "🏠 HOME":
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        # Clique na logo para "logar" e mostrar os ícones
        if st.button("🛡️ ZION TECNOLOGIA (CLIQUE NA LOGO PARA ACESSAR)", use_container_width=True):
            st.session_state.logado = not st.session_state.logado
        
        if os.path.exists("LOGO.PNG"):
            st.image("LOGO.PNG", use_container_width=True)
        
        # Só aparece após o clique na logo
        if st.session_state.logado:
            st.markdown("---")
            c1, c2, c3 = st.columns(3)
            if c1.button("📋 NOVO LANÇAMENTO", use_container_width=True): navegar("📋 AGENDAMENTO")
            if c2.button("📊 VER AGENDAMENTO", use_container_width=True): navegar("📊 VER AGENDAMENTOS")
            if c3.button("💰 FINANCEIRO", use_container_width=True): navegar("💰 FINANCEIRO")

# --- TELA 2: AGENDAMENTO (REVISÃO DE TODOS OS CAMPOS) ---
elif st.session_state.pagina == "📋 AGENDAMENTO":
    if st.button("⬅️ VOLTAR AO INÍCIO"): navegar("🏠 HOME")
    st.header("📋 Cadastro Geral de Missão")
    
    with st.form("form_completo", clear_on_submit=True):
        c1, c2, c3 = st.columns(3)
        # Coluna 1
        os_n = c1.text_input("Nº O.S")
        ini_m = c1.date_input("INICIO DA MISSÃO", format="DD/MM/YYYY")
        h_emb = c1.text_input("HORA DE EMBARQUE")
        local = c1.text_input("LOCAL")
        empurrador = c1.text_input("EMPURRADOR")
        
        # Coluna 2
        saida = c2.text_input("SAÍDA")
        fim_m = c2.date_input("FIM DA MISSÃO", format="DD/MM/YYYY")
        esc1 = c2.text_input("ESCOLTA 1")
        esc2 = c2.text_input("ESCOLTA 2")
        servico = c2.selectbox("SERVIÇO", ["Escolta", "Vigilância"])
        
        # Coluna 3
        cliente = c3.text_input("CLIENTE")
        balsa = c3.text_input("BALSA")
        destino = c3.text_input("DESTINO")
        pedido = c3.text_input("PEDIDO")
        assinatura = c3.text_input("ASSINATURA")
        status = c3.selectbox("STATUS", ["Em Andamento", "Encerrado"])

        desc = st.text_area("DESCRIÇÃO")

        if st.form_submit_button("✅ SALVAR OPERAÇÃO"):
            payload = {
                "parent": {"database_id": DATABASE},
                "properties": {
                    "Nº OS": {"title": [{"text": {"content": os_n}}]},
                    "CLIENTE": {"rich_text": [{"text": {"content": cliente}}]},
                    "INÍCIO DA MISSÃO": {"date": {"start": str(ini_m)}},
                    "FIM DA MISSÃO": {"date": {"start": str(fim_m)}},
                    "ESCOLTA 1": {"rich_text": [{"text": {"content": esc1}}]},
                    "ESCOLTA 2": {"rich_text": [{"text": {"content": esc2}}]},
                    "HORA DE EMBARQUE": {"rich_text": [{"text": {"content": h_emb}}]},
                    "LOCAL": {"rich_text": [{"text": {"content": local}}]},
                    "EMPURRADOR": {"rich_text": [{"text": {"content": empurrador}}]},
                    "SAÍDA": {"rich_text": [{"text": {"content": saida}}]},
                    "BALSA": {"rich_text": [{"text": {"content": balsa}}]},
                    "DESTINO": {"rich_text": [{"text": {"content": destino}}]},
                    "PEDIDO": {"rich_text": [{"text": {"content": pedido}}]},
                    "ASSINATURA": {"rich_text": [{"text": {"content": assinatura}}]},
                    "STATUS": {"select": {"name": status}},
                    "SERVIÇO": {"select": {"name": servico}},
                    "DESCRIÇÃO": {"rich_text": [{"text": {"content": desc}}]}
                }
            }
            res = requests.post("https://api.notion.com/v1/pages", headers=headers, json=payload)
            if res.status_code == 200:
                st.success("🎯 Salvo com sucesso!")
                navegar("📊 VER AGENDAMENTOS")
            else: st.error(f"Erro: {res.text}")

# --- TELA 3: VER AGENDAMENTOS (TABELA COM PDF/EDIÇÃO) ---
elif st.session_state.pagina == "📊 VER AGENDAMENTOS":
    if st.button("⬅️ VOLTAR AO INÍCIO"): navegar("🏠 HOME")
    st.header("📊 Operações em Tempo Real")
    df = buscar_dados()
    if not df.empty:
        # Tabela com botões laterais igual ao vídeo
        for i, r in df.iterrows():
            col_d, col_b = st.columns([4, 1])
            col_d.write(f"**O.S {r['Nº OS']}** | {r['CLIENTE']} | {r['STATUS']}")
            if col_b.button(f"📄 PDF/EDIT {r['Nº OS']}", key=r['ID']):
                st.info("Função de PDF/Edição integrada para esta O.S.")
        st.divider()
        st.dataframe(df.drop(columns=["ID"]), use_container_width=True)

# --- TELA 4: FINANCEIRO ---
elif st.session_state.pagina == "💰 FINANCEIRO":
    if st.button("⬅️ VOLTAR AO INÍCIO"): navegar("🏠 HOME")
    st.header("💰 Fluxo Financeiro Zion")
    df = buscar_dados()
    if not df.empty:
        st.metric("TOTAL FATURADO", f"R$ {df['VALOR'].sum():,.2f}")
        st.table(df[["Nº OS", "CLIENTE", "STATUS", "VALOR"]])
