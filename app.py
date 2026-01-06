def gerar_pdf(d):
    pdf = FPDF()
    pdf.add_page()
    
    # --- LOGO / CABEÇALHO ---
    # Se você tiver a imagem combinada das logos, use pdf.image("logos_topo.png", x=10, y=8, w=60)
    pdf.set_font("Arial", "B", 8)
    pdf.cell(0, 5, "ZION TECNOLOGIA | TRANSDOURADA", ln=True, align="L")
    pdf.set_font("Arial", "", 7)
    pdf.cell(0, 5, "Navegação Ltda.    GRUPO DIAS", ln=True, align="L")
    pdf.ln(10)

    # --- TÍTULOS ---
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Solicitação de Escolta", ln=True, align="C")
    pdf.set_font("Arial", "B", 11)
    pdf.cell(0, 7, "ORDEM DE SERVIÇO", ln=True, align="C")
    pdf.cell(0, 7, f"O.S: {d['Nº OS']}", ln=True, align="C")
    
    pdf.set_font("Arial", "", 10)
    pdf.cell(0, 7, f"STATUS: {d['STATUS']}", ln=True, align="C")
    pdf.ln(2)

    # --- CAIXA SOLICITANTE ---
    pdf.set_fill_color(255, 255, 255)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, f"SOLICITANTE ( {d['CLIENTE']} )", border=1, ln=True, align="C")
    pdf.ln(5)

    # --- GRID DE INFORMAÇÕES (LINHA 1) ---
    pdf.set_font("Arial", "", 9)
    # Usando multi-colunas simuladas por coordenadas
    y_topo = pdf.get_y()
    pdf.text(10, y_topo, f"EMPURRADOR:  {d.get('EMPURRADOR', '---')}")
    pdf.text(80, y_topo, f"SAÍDA PREVISTA:  {d.get('HORA_EMBARQUE', '---')}")
    pdf.text(150, y_topo, f"STATUS: {d['STATUS']}")
    
    # LINHA 2
    pdf.text(10, y_topo + 5, f"SAÍDA PREVISTA: CLIENTE")
    pdf.text(80, y_topo + 5, f"EMBARQUE:")
    
    # LINHA 3 (ORIGEM / DESTINO)
    pdf.text(10, y_topo + 10, f"ORIGEM: {d.get('LOCAL', '---')}")
    pdf.text(80, y_topo + 10, f"DESTINO: {d.get('DESTINO', '---')}")
    pdf.text(150, y_topo + 10, f"SERVIÇO: {d['SERVIÇO']}")
    
    # LINHA 4 (BALSA)
    pdf.text(10, y_topo + 15, f"BALSA: {d.get('BALSA', '---')}")
    pdf.text(150, y_topo + 15, f"SERVIÇO: {d['SERVIÇO']}")
    
    pdf.set_y(y_topo + 25)

    # --- CAIXA EMPRESA VIGILÂNCIA ---
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "PVH-SEG Serv. de Vig. Patrimonial Ltda", border=1, ln=True, align="C")
    pdf.ln(5)

    # --- DATAS E ESCOLTAS ---
    pdf.set_font("Arial", "", 10)
    pdf.cell(0, 6, f"INÍCIO DA MISSÃO: {d['INÍCIO']}", ln=True)
    pdf.cell(0, 6, f"ESCOLTA 1: {d.get('ESCOLTA 1', '---')}", ln=True)
    pdf.cell(0, 6, f"ESCOLTA 2: {d.get('ESCOLTA 2', '---')}", ln=True)
    pdf.cell(0, 6, f"FIM DA MISSÃO: {d['DT SAÍDA']}", ln=True)
    
    pdf.ln(5)
    pdf.cell(0, 0, "", border="T", ln=True) # Linha divisória tracejada
    pdf.ln(5)

    # --- DETALHAMENTO ---
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "DETALHAMENTO DA MISSÃO.", ln=True, align="C")
    pdf.ln(2)
    
    pdf.set_font("Arial", "", 11)
    # Multi_cell para o texto quebrar linha automaticamente como na imagem
    descricao_texto = f"DESCRIÇÃO: {d.get('DESCRIÇÃO', 'Sem observações adicionais.')}"
    pdf.multi_cell(0, 6, descricao_texto)

    # --- ASSINATURA ---
    pdf.set_y(-60) # Posiciona no final da página
    pdf.cell(0, 0, "", border="T", ln=True)
    pdf.set_font("Arial", "", 8)
    pdf.cell(0, 10, "ASSINATURA RESPONSÁVEL", ln=True, align="L")
    
    # --- RODAPÉ ---
    pdf.set_y(-30)
    pdf.set_font("Arial", "B", 8)
    pdf.cell(0, 4, "TRANSDOURADA NAVEGAÇÃO LTDA 01.269.7300001-74 ROD BR 316 KM 08, SN", ln=True, align="C")
    pdf.cell(0, 4, "AGUA BRANCA 67033- 970 ANANINDEUA", ln=True, align="C")

    return pdf.output(dest="S").encode("latin-1")
