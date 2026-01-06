import streamlit as st
import requests
import pandas as pd
import os

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

# --- FUNÇÕES DE APOIO ---
def buscar_dados():
    url = f"https://api.notion.com/v1/databases/{DATABASE}/query"
    res = requests.post(url, headers=headers)
    if res.status_code == 200:
        dados = res.json()["results"]
        lista = []
        for pg in dados:
            p = pg["properties"]
            try:
                # Lógica Financeira: Escolta (1870) | Vigilância (970)
                servico_tipo = p.get("SERVIÇO", {}).get("select", {}).get("name", "Escolta")
                valor_unitario = 1870.0 if servico_tipo == "Escolta" else 970.0
                
                lista.append({
                    "ID": pg["id"],
                    "Nº OS": p.get("Nº OS", {}).get("title", [{}])[0].get("text", {}).get("content", ""),
                    "CLIENTE": p.get("CLIENTE", {}).get("rich_text", [{}])[0].get("text", {}).get("content", ""),
                    "INÍCIO": p.get("INÍCIO DA MISSÃO", {}).get("date", {}).get("start", ""),
                    "SERVIÇO": servico_tipo,
                    "STATUS": p.get("STATUS", {}).get("select", {}).get("name", "Em Andamento"),
                    "BALSA": p.get("BALSA", {}).get("rich_text", [{}])[0].get("text", {}).get("content", ""),
                    "VALOR": valor_unitario
                })
            except: continue
        return pd.DataFrame(lista)
    return pd.DataFrame()

# --- CONTROLE DE NAVEGAÇÃO ---
if "pagina" not in st.session_state:
    st.session_state.pagina = "🏠 HOME"

def navegar_para(destino):
    st.session_state.pagina = destino
    st.rerun()

# --- BARRA LATERAL ---
with st.sidebar:
    if os.path.exists("LOGO.PNG"):
        if st.button("🏠 SISTEMA ZION (HOME)", use_container_width=True):
            navegar_para("🏠 HOME")
        st.image("LOGO.PNG", use_container_width=True)
    
    st.markdown("---")
    menu = st.radio("NAVEGAÇÃO", ["🏠 HOME", "📋 AGENDAMENTO ZION", "📊 VER AGENDAMENTOS", "💰 FINANCEIRO"])
    if menu != st.session_state.pagina:
        navegar_para(menu)

# --- TELA 1: HOME (ABERTURA CLICÁVEL) ---
if st.session_state.pagina == "🏠 HOME":
    st.title("🛡️ Zion Tecnologia - Gestão de Escolta")
    st.subheader("Bem-vindo ao Painel Principal")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📋 NOVO AGENDAMENTO", use_container_width=True): navegar_para("📋 AGENDAMENTO ZION")
    with col2:
        if st.button("📊 VER AGENDAMENTOS", use_container_width=True): navegar_para("📊 VER AGENDAMENTOS")
    with col3:
        if st.button("💰 FINANCEIRO", use_container_width=True): navegar_para("💰 FINANCEIRO")
    
    st.markdown("---")
    # Logo Principal Clicável (Simulado por botão)
    if st.button("🚀 CLIQUE AQUI PARA INICIAR LANÇAMENTO", use_container_width=True):
        navegar_para("📋 AGENDAMENTO ZION")
    st.image("LOGO.PNG", width=600)

# --- TELA 2: AGENDAMENTO ---
elif st.session_state.pagina == "📋 AGENDAMENTO ZION":
    st.header("📋 Lançamento de Missão")
    if st.button("⬅️ VOLTAR AO INÍCIO"): navegar_para("🏠 HOME")
    
    with st.form("form_registro", clear_on_submit=True):
        c1, c2, c3 = st.columns(3)
        os_v = c1.text_input("Nº OS")
        servico = c1.selectbox("TIPO DE SERVIÇO", ["Escolta", "Vigilância"])
        dt_ini = c1.date_input("INÍCIO DA MISSÃO", format="DD/MM/YYYY")
        
        cli = c2.text_input("CLIENTE")
        esc1 = c2.text_input("ESCOLTA 1")
        esc2 = c2.text_input("ESCOLTA 2")
        
        status = c3.selectbox("STATUS DA OPERAÇÃO", ["Em Andamento", "Encerrado"])
        balsa = c3.text_input("BALSA")
        destino = c3.text_input("DESTINO")
        
        c4, c5 = st.columns(2)
        pedido = c4.text_input("Nº PEDIDO")
        assinatura = c5.text_input("ASSINATURA RESPONSÁVEL")
        
        desc = st.text_area("DETALHAMENTO / OBSERVAÇÕES")

        if st.form_submit_button("✅ SALVAR E VER AGENDAMENTOS"):
            payload = {
                "parent": {"database_id": DATABASE},
                "properties": {
                    "Nº OS": {"title": [{"text": {"content": os_v}}]},
                    "CLIENTE": {"rich_text": [{"text": {"content": cli}}]},
                    "SERVIÇO": {"select": {"name": servico}},
                    "STATUS": {"select": {"name": status}},
                    "INÍCIO DA MISSÃO": {"date": {"start": str(dt_ini)}},
                    "ESCOLTA 1": {"rich_text": [{"text": {"content": esc1}}]},
                    "ESCOLTA 2": {"rich_text": [{"text": {"content": esc2}}]},
                    "BALSA": {"rich_text": [{"text": {"content": balsa}}]},
                    "DESTINO": {"rich_text": [{"text": {"content": destino}}]},
                    "PEDIDO": {"rich_text": [{"text": {"content": pedido}}]},
                    "ASSINATURA": {"rich_text": [{"text": {"content": assinatura}}]},
                    "DESCRIÇÃO": {"rich_text": [{"text": {"content": desc}}]}
                }
            }
            res = requests.post("https://api.notion.com/v1/pages", headers=headers, json=payload)
            if res.status_code == 200:
                st.success("🎯 Salvo com sucesso!")
                navegar_para("📊 VER AGENDAMENTOS")
            else:
                st.error(f"Erro no Notion: {res.text}")

# --- TELA 3: VER AGENDAMENTOS (TABELA COM AÇÕES) ---
elif st.session_state.pagina == "📊 VER AGENDAMENTOS":
    st.header("📊 Operações em Tempo Real")
    if st.button("⬅️ VOLTAR AO INÍCIO"): navegar_para("🏠 HOME")
    
    df = buscar_dados()
    if not df.empty:
        # Layout de cartões/linhas para botões de PDF
        for _, row in df.iterrows():
            with st.expander(f"📦 O.S: {row['Nº OS']} - {row['CLIENTE']} ({row['STATUS']})"):
                col_a, col_b, col_c = st.columns(3)
                col_a.write(f"**Início:** {row['INÍCIO']}")
                col_b.write(f"**Balsa:** {row['BALSA']}")
                col_c.write(f"**Valor:** R$ {row['VALOR']:,.2f}")
                
                # Ações integradas
                btn_col1, btn_col2 = st.columns(2)
                if btn_col1.button(f"🖨️ GERAR PDF {row['Nº OS']}", key=f"pdf_{row['ID']}"):
                    st.toast("Gerando PDF profissional...")
                if btn_col2.button(f"📝 EDITAR STATUS", key=f"edit_{row['ID']}"):
                    st.warning("Função de edição rápida em desenvolvimento.")
        
        st.divider()
        st.dataframe(df.drop(columns=["ID"]), use_container_width=True, hide_index=True)
    else:
        st.info("Nenhum registro encontrado.")

# --- TELA 4: FINANCEIRO (TABELA DETALHADA) ---
elif st.session_state.pagina == "💰 FINANCEIRO":
    st.header("💰 Fluxo Financeiro por Operação")
    if st.button("⬅️ VOLTAR AO INÍCIO"): navegar_para("🏠 HOME")
    
    df = buscar_dados()
    if not df.empty:
        # Mostra o valor total acumulado
        total_geral = df["VALOR"].sum()
        st.metric("FATURAMENTO TOTAL ACUMULADO", f"R$ {total_geral:,.2f}")
        
        # Tabela detalhada
        df_fin = df[["Nº OS", "CLIENTE", "SERVIÇO", "STATUS", "VALOR"]]
        st.table(df_fin)
    else:
        st.info("Aguardando lançamentos para calcular financeiro.")
