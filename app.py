import streamlit as st
import pandas as pd
from fpdf import FPDF
import os

# --- FUNÇÃO PDF EM FORMATO A4 COM LOGO ---
def gerar_pdf_a4(dados):
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.add_page()
    
    # Adicionando a Logo no Topo
    if os.path.exists("LOGO.PNG"):
        pdf.image("LOGO.PNG", x=10, y=8, w=40)
    
    # Cabeçalho da Empresa
    pdf.set_font("Arial", 'B', 18)
    pdf.cell(0, 15, "ZION TECNOLOGIA", ln=True, align='C')
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "ORDEM DE SERVIÇO - COMPROVANTE OPERACIONAL", ln=True, align='C')
    pdf.ln(10)
    
    # Linha divisória
    pdf.line(10, 45, 200, 45)
    pdf.ln(5)

    # Conteúdo da O.S em Tabela Formatada
    pdf.set_font("Arial", 'B', 10)
    pdf.set_fill_color(230, 230, 230)
    
    # Organizando os dados em pares para preencher o A4
    itens = list(dados.items())
    for i in range(0, len(itens), 2):
        # Campo 1
        pdf.cell(45, 10, txt=f"{itens[i][0]}:", border=1, fill=True)
        pdf.cell(50, 10, txt=f"{itens[i][1]}", border=1)
        
        # Campo 2 (se houver)
        if i + 1 < len(itens):
            pdf.cell(45, 10, txt=f"{itens[i+1][0]}:", border=1, fill=True)
            pdf.cell(50, 10, txt=f"{itens[i+1][1]}", border=1)
        pdf.ln()

    # Rodapé com assinatura
    pdf.ln(30)
    pdf.line(20, pdf.get_y(), 90, pdf.get_y())
    pdf.line(120, pdf.get_y(), 190, pdf.get_y())
    pdf.set_font("Arial", 'I', 8)
    pdf.cell(90, 10, "ASSINATURA RESPONSÁVEL", 0, 0, 'C')
    pdf.cell(90, 10, "ASSINATURA COLABORADOR", 0, 0, 'C')

    return pdf.output(dest='S').encode('latin-1')

# --- O RESTANTE DO CÓDIGO PERMANECE IGUAL, APENAS ATUALIZE A TELA DE AGENDAMENTO ---

if st.session_state.tela == "AGENDAMENTO":
    st.title("⏳ Agendamento de Missões (A4 Disponível)")
    if st.session_state.db_os:
        df = pd.DataFrame(st.session_state.db_os)
        
        # Tabela Operacional
        cols_op = ["O.S", "PEDIDO", "INÍCIO", "FIM", "EMPURRADOR", "LOCAL", "STATUS"]
        st.dataframe(df[cols_op], use_container_width=True)
        
        st.divider()
        st.subheader("🖨️ Impressão de O.S em Formato A4")
        
        for i, row in df.iterrows():
            with st.expander(f"Visualizar e Baixar O.S {row['O.S']}"):
                col_txt, col_btn = st.columns([7, 3])
                col_txt.write(f"**Relatório Pronto para Impressão:** {row['PEDIDO']} - {row['EMPURRADOR']}")
                
                # Chama a nova função A4
                pdf_bytes = gerar_pdf_a4(row.to_dict())
                
                col_btn.download_button(
                    label="📂 BAIXAR O.S EM A4",
                    data=pdf_bytes,
                    file_name=f"OS_ZION_{row['O.S']}.pdf",
                    mime="application/pdf",
                    key=f"btn_a4_{i}"
                )
    else:
        st.info("Nenhuma O.S registrada.")
