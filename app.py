import streamlit as st
import requests
import pandas as pd
import os
from fpdf import FPDF
from datetime import datetime

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Zion Tecnologia", layout="wide")

# --- CONEXÃO NOTION ---
TOKEN = st.secrets["notion"]["token"].replace('"', '').strip()
DATABASE = st.secrets["notion"]["database_id"].replace('"', '').strip()

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

# --- FUNÇÃO CARREGAR DADOS (COM DIAGNÓSTICO) ---
def carregar_dados_notion():
    try:
        # Busca sem filtros para garantir que TUDO apareça
        res = requests.post(f"https://api.notion.com/v1/databases/{DATABASE}/query", headers=headers)
        if res.status_code == 200:
            results = res.json().get("results", [])
            if not results:
                return []
                
            lista = []
            for r in results:
                p = r["properties"]
                
                # Funções de segurança para ler dados
                def get_title(n): return p[n]["title"][0]["plain_text"] if n in p and p[n]["title"] else "---"
                def get_text(n): return p[n]["rich_text"][0]["plain_text"] if n in p and p[n]["rich_text"] else "---"
                def get_date(n): 
                    try: return datetime.strptime(p[n]["date"]["start"], '%Y-%m-%d').strftime('%d/%m/%Y') if n in p and p[n]["date"] else "---"
                    except: return "---"
                def get_sel(n): return p[n]["select"]["name"] if n in p and p[n]["select"] else "---"

                lista.append({
                    "ID": r["id"],
                    "Nº OS": get_title("Nº OS"),
                    "CLIENTE": get_text("CLIENTE"),
                    "DT SAÍDA": get_date("DT SAÍDA"),
                    "STATUS": get_sel("STATUS"),
                    "EMPURRADOR": get_text("EMPURRADOR"),
                    "BALSA": get_text("BALSA"),
                    "LOCAL": get_text("LOCAL"),
                    "DESTINO": get_text("DESTINO"),
                    "HORA_EMBARQUE": get_text("HORA DE EMBARQUE"),
                    "ESCOLTA 1": get_text("ESCOLTA 1"),
                    "ESCOLTA 2": get_text("ESCOLTA 2"),
                    "DESCRIÇÃO": get_text("DESCRIÇÃO"),
                    "PEDIDO": get_text("PEDIDO"),
                    "INÍCIO": get_date("INÍCIO DA MISSÃO"),
                    "FIM": get_date("FIM DA MISSÃO"),
                    "ASSINATURA": get_text("ASSINATURA RESPONSÁVEL")
                })
            return lista
        else:
            st.error(f"Erro de Conexão: {res.status_code}")
            return []
    except Exception as e:
        st.error(f"Erro ao processar dados: {e}")
        return []

# --- NAVEGAÇÃO ---
if "pagina" not in st.session_state: st.session_state.pagina = "🏠 HOME"
if "dados_edicao" not in st.session_state: st.session_state.dados_edicao = None

def navegar(p):
    st.session_state.pagina = p
    st.rerun()

# --- TELA GRADE (A TELA QUE NÃO ESTAVA MOSTRANDO) ---
if st.session_state.pagina == "📊 GRADE":
    st.title("📊 Agendamentos Ativos")
    if st.button("⬅️ VOLTAR PARA HOME"): 
        navegar("🏠 HOME")
    
    with st.spinner("Buscando dados no Notion..."):
        dados = carregar_dados_notion()
    
    if dados:
        # Transforma em Tabela
        df = pd.DataFrame(dados)
        
        # Mostra a tabela principal
        st.subheader("Lista Geral")
        st.dataframe(df[["Nº OS", "CLIENTE", "DT SAÍDA", "STATUS"]], use_container_width=True)
        
        st.markdown("---")
        st.subheader("Ações e Detalhes")
        
        # Cria os botões para cada item
        for d in dados:
            with st.expander(f"⚙️ OS {d['Nº OS']} - {d['CLIENTE']}"):
                c1, c2 = st.columns(2)
                if c1.button(f"✏️ EDITAR {d['Nº OS']}", key=f"edit_{d['ID']}"):
                    st.session_state.dados_edicao = d
                    st.session_state.pagina = "📋 CADASTRO"
                    st.rerun()
                
                # Botão de PDF aqui também
                st.write(f"**Empurrador:** {d['EMPURRADOR']} | **Balsa:** {d['BALSA']}")
    else:
        st.warning("⚠️ Nenhuma Ordem de Serviço encontrada na base de dados do Notion.")
        st.info("Dica: Verifique se a integração no Notion está 'Conectada' a esta página da base de dados.")

# (O restante do código de Cadastro e Home segue o mesmo padrão anterior)
