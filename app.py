import streamlit as st
import requests
from fpdf import FPDF

st.set_page_config(page_title="Zion Tecnologia", layout="wide")

# Limpeza automática de segurança
TOKEN = st.secrets["notion"]["token"].replace('"', '').replace('\\', '').strip()
DATABASE = st.secrets["notion"]["database_id"].replace('"', '').replace('\\', '').strip()

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

# Funções auxiliares
def buscar_dados():
    try:
        url = f"https://api.notion.com/v1/databases/{DATABASE}/query"
        res = requests.post(url, headers=headers)
        if res.status_code == 200:
            results = res.json().get("results", [])
            paginas = []
            for page in results:
                p = page["properties"]
                os_val = p["Nº OS"]["title"][0]["text"]["content"] if p["Nº OS"]["title"] else "S/N"
                cli_val = p["CLIENTE"]["rich_text"][0]["text"]["content"] if p["CLIENTE"]["rich_text"] else ""
                paginas.append({"id": page["id"], "os": os_val, "cliente": cli_val, "full": p})
            return paginas
    except: return []
    return []

def gerar_pdf(dados):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, "ZION TECNOLOGIA - ORDEM DE SERVIÇO", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", size=12)
    for k, v in dados.items():
        pdf.cell(200, 8, f"{k}: {v}", ln=True)
    return pdf.output(dest='S').encode('latin-1')

st.title("🚨 Sistema Zion")

aba1, aba2 = st.tabs(["🆕 Nova OS", "✏️ Editar e PDF"])

with aba1:
    with st.form("form_nova", clear_on_submit=True):
        c1, c2 = st.columns(2)
        os_n = c1.text_input("Nº OS")
        cli_n = c1.text_input("CLIENTE")
        ped_n = c2.text_input("PEDIDO")
        tipo_n = c2.selectbox("TIPO", ["ESCOLTA", "VIGILÂNCIA", "OUTROS"])
        desc_n = st.text_area("DESCRIÇÃO")
        if st.form_submit_button("✅ SALVAR"):
            payload = {
                "parent": {"database_id": DATABASE},
                "properties": {
                    "Nº OS": {"title": [{"text": {"content": os_n}}]},
                    "CLIENTE": {"rich_text": [{"text": {"content": cli_n}}]},
                    "PEDIDO": {"rich_text": [{"text": {"content": ped_n}}]},
                    "TIPO": {"select": {"name": tipo_n}},
                    "DESCRIÇÃO": {"rich_text": [{"text": {"content": desc_n}}]}
                }
            }
            res = requests.post("https://api.notion.com/v1/pages", headers=headers, json=payload)
            if res.status_code == 200: st.success("🎯 Salvo!")
            else: st.error(f"Erro: {res.text}")

with aba2:
    dados_lista = buscar_dados()
    if dados_lista:
        dict_os = {f"OS {d['os']} - {d['cliente']}": d for d in dados_lista}
        escolha = st.selectbox("Selecione a OS para Ações", list(dict_os.keys()))
        
        if escolha:
            selecionado = dict_os[escolha]
            
            # Form de edição (sem o botão de download dentro)
            with st.form("form_edicao"):
                st.write(f"--- Editando OS: {selecionado['os']} ---")
                ed_cli = st.text_input("Cliente", value=selecionado['cliente'])
                ed_desc = st.text_area("Descrição")
                
                if st.form_submit_button("💾 SALVAR ALTERAÇÕES"):
                    url_update = f"https://api.notion.com/v1/pages/{selecionado['id']}"
                    up_payload = {"properties": {"CLIENTE": {"rich_text": [{"text": {"content": ed_cli}}]}}}
                    requests.patch(url_update, headers=headers, json=up_payload)
                    st.success("Atualizado!")
                    st.rerun()

            # BOTÃO DE PDF FORA DO FORMULÁRIO (Para evitar o erro)
            st.write("--- Exportar ---")
            pdf_data = {"OS": selecionado['os'], "Cliente": selecionado['cliente']}
            pdf_bytes = gerar_pdf(pdf_data)
            st.download_button(
                label="📄 BAIXAR PDF DA ORDEM",
                data=pdf_bytes,
                file_name=f"OS_{selecionado['os']}.pdf",
                mime="application/pdf"
            )
    else:
        st.info("Nenhuma OS encontrada para editar.")
