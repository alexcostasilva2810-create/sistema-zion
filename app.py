import streamlit as st
import os
import requests

# --- 1. CONFIGURAÇÃO INICIAL ---
st.set_page_config(page_title="Zion Business", layout="wide", initial_sidebar_state="collapsed")

# Chaves do Notion (COLOQUE AS SUAS AQUI)
NOTION_TOKEN = "SEU_TOKEN_AQUI"
DATABASE_ID = "SEU_ID_DA_TABELA_AQUI"

if 'pagina' not in st.session_state:
    st.session_state.pagina = "🏠 HOME"

# --- 2. ESTILO CSS (Labels Brancas / Texto Digitado Preto) ---
st.markdown("""
<style>
    .stApp { background-color: #000b1a; color: white; }
    [data-testid="stSidebar"], .stHeader, .stFooter { display: none !important; }
    .welcome-text { font-size: 45px; font-weight: 800; text-align: center; text-shadow: 0px 0px 20px #0096ff; }
    
    /* Nomes dos campos em BRANCO */
    label { color: white !important; font-weight: bold !important; }
    
    /* Texto digitado em PRETO dentro das caixas brancas */
    input, select, textarea { color: black !important; background-color: white !important; }
    
    /* Botões da Home */
    div.stButton > button {
        width: 100% !important; height: 65px !important;
        background: linear-gradient(145deg, #0096ff, #005bb5) !important;
        color: white !important; border-radius: 40px 8px 40px 8px !important;
        box-shadow: 0px 8px 0px #003d66 !important; margin-bottom: 15px !important;
    }
    .footer-zion { position: fixed; bottom: 20px; left: 40px; color: #0096ff; font-weight: bold; letter-spacing: 2px; }
</style>
""", unsafe_allow_html=True)

# --- 3. NAVEGAÇÃO ---

if st.session_state.pagina == "🏠 HOME":
    st.markdown('<div class="welcome-text">Seja Bem Vindo ao Futuro</div>', unsafe_allow_html=True)
    col_btns, col_robo = st.columns([1, 1.2], gap="large")
    
    with col_btns:
        st.write("##")
        if st.button("🚀 LANÇAMENTO"):
            st.session_state.pagina = "LANÇAMENTO"
            st.rerun()
        if st.button("🛠️ ORDEM DE SERVIÇO"):
            st.session_state.pagina = "OS"; st.rerun()
        if st.button("💰 FINANCEIRO"):
            st.session_state.pagina = "FINANCEIRO"; st.rerun()
        if st.button("📊 EXTRATO"):
            st.session_state.pagina = "EXTRATO"; st.rerun()

    with col_robo:
        if os.path.exists("robo_humanizado.jpg"):
            st.image("robo_humanizado.jpg", use_container_width=True)
    st.markdown('<div class="footer-zion">ZION GESTÃO DE ESCOLTA</div>', unsafe_allow_html=True)

elif st.session_state.pagina == "LANÇAMENTO":
    st.markdown('<div class="welcome-text" style="font-size:35px;">🚀 Ordens de Serviço</div>', unsafe_allow_html=True)
    
    if st.button("⬅️ VOLTAR PARA HOME"):
        st.session_state.pagina = "🏠 HOME"; st.rerun()

    with st.form("form_zion"):
        c1, c2, c3 = st.columns(3)
        with c1:
            f1_os = st.text_input("1. Nº O.S.")
            f2_cliente = st.text_input("2. CLIENTE")
            f3_inicio = st.date_input("3. INÍCIO DA MISSÃO", format="DD/MM/YYYY")
            f4_tipo = st.selectbox("4. TIPO", ["Ostensiva", "Velada", "Fixo"])
            f5_embarque = st.time_input("5. HORA DE EMBARQUE")
            f6_local = st.text_input("6. LOCAL")
        with c2:
            f7_empurrador = st.text_input("7. EMPURRADOR")
            f8_dt_saida = st.date_input("8. DT SAÍDA", format="DD/MM/YYYY")
            f9_fim = st.date_input("9. FIM DA MISSÃO", format="DD/MM/YYYY")
            f10_status = st.selectbox("10. STATUS", ["Em Andamento", "Encerrado", "Cancelado"])
            f11_servico = st.text_input("11. SERVIÇO")
            f12_escolta1 = st.text_input("12. ESCOLTA 1")
        with c3:
            f13_escolta2 = st.text_input("13. ESCOLTA 2")
            f14_balsa = st.text_input("14. BALSA")
            f15_destino = st.text_input("15. DESTINO")
            f16_desc = st.text_area("16. DESCRIÇÃO")
            f17_assinatura = st.text_input("17. ASSINATURA")

        if st.form_submit_button("💾 SALVAR NO NOTION"):
            headers = {"Authorization": f"Bearer {NOTION_TOKEN}", "Content-Type": "application/json", "Notion-Version": "2022-06-28"}
            payload = {
                "parent": {"database_id": DATABASE_ID},
                "properties": {
                    "Nº O.S.": {"title": [{"text": {"content": f1_os}}]},
                    "CLIENTE": {"rich_text": [{"text": {"content": f2_cliente}}]},
                    "INÍCIO DA MISSÃO": {"date": {"start": f3_inicio.isoformat()}},
                    "STATUS": {"select": {"name": f10_status}},
                    "LOCAL": {"rich_text": [{"text": {"content": f6_local}}]}
                    # Adicione os outros campos conforme a estrutura da sua tabela
                }
            }
            res = requests.post("https://api.notion.com/v1/pages", headers=headers, json=payload)
            if res.status_code == 200:
                st.success("✅ Salvo com sucesso!")
            else:
                st.error(f"Erro: {res.text}")

    st.markdown('<div class="footer-zion">ZION GESTÃO DE ESCOLTA</div>', unsafe_allow_html=True)
