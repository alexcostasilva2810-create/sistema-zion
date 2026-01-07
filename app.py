# --- NOVA FUNÇÃO PDF (O.S INDIVIDUAL) ---
def gerar_pdf_os_novo(d):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # --- FUNÇÕES AUXILIARES DE DESENHO ---
    def draw_header():
        logo_path = "logo_transdourada.png"
        if os.path.exists(logo_path):
            c.drawImage(logo_path, 2 * cm, height - 3 * cm, width=5*cm, preserveAspectRatio=True, mask='auto')
        else:
            c.setFont("Helvetica-Bold", 14)
            c.drawString(2 * cm, height - 2 * cm, "TRANSDOURADA Navegação Ltda.")
        
        c.setFont("Helvetica-Bold", 16)
        c.drawCentredString(width / 2, height - 4.5 * cm, "Solicitação de Escolta")

    def draw_os_details():
        c.setFont("Helvetica", 11)
        c.drawCentredString(width / 2, height - 5.5 * cm, f"ORDEM DE SERVIÇO O.S: {d.get('Nº OS', 'N/A')}")
        c.drawCentredString(width / 2, height - 6 * cm, f"STATUS: {d.get('STATUS', 'N/A').upper()}")
        
        c.setStrokeColor(black)
        c.rect(4 * cm, height - 7 * cm, width - 8 * cm, 0.8 * cm, stroke=1, fill=0)
        c.setFont("Helvetica-Bold", 12)
        c.drawCentredString(width / 2, height - 6.7 * cm, "SOLICITANTE ( TRANSDOURADA )")

    def draw_info_section():
        c.setFont("Helvetica-Bold", 10)
        start_y = height - 8.5 * cm
        x_label = 2.5 * cm
        x_value = 5.5 * cm
        
        data_map = {
            "EMPURRADOR:": d.get('EMPURRADOR', ''),
            "SAÍDA PREVISTA:": d.get('HORA_EMBARQUE', ''),
            "ORIGEM:": d.get('LOCAL', ''),
            "DESTINO:": d.get('DESTINO', ''),
            "BALSA:": d.get('BALSA', ''),
            "CLIENTE:": d.get('CLIENTE', ''),
            "CMT:": ""
        }
        
        line_height = 0.6 * cm
        for i, (label, value) in enumerate(data_map.items()):
            c.drawString(x_label, start_y - (i * line_height), label)
            c.setFont("Helvetica", 10)
            c.drawString(x_value, start_y - (i * line_height), str(value)) # Usei str() para segurança
            c.setFont("Helvetica-Bold", 10)

    def draw_mission_section():
        c.setStrokeColor(black)
        c.rect(4 * cm, height - 14 * cm, width - 8 * cm, 0.8 * cm, stroke=1, fill=0)
        c.setFont("Helvetica-Bold", 12)
        c.drawCentredString(width / 2, height - 13.7 * cm, "PVH-SEG Serv. de Vig.Patrimonial Ltda")

        c.setFont("Helvetica", 10)
        start_y = height - 15.5 * cm
        x_pos = 2.5 * cm
        line_height = 0.6 * cm
        
        inicio_missao = datetime.strptime(d['INÍCIO'], '%Y-%m-%d').strftime('%d/%m/%Y') if d.get('INÍCIO') else 'N/A'
        fim_missao = datetime.strptime(d['FIM'], '%Y-%m-%d').strftime('%d/%m/%Y') if d.get('FIM') else 'N/A'

        c.drawString(x_pos, start_y, f"INÍCIO DA MISSÃO: {inicio_missao}")
        c.drawString(x_pos, start_y - line_height, f"ESCOLTA 1: {d.get('ESCOLTA 1', '')}")
        c.drawString(x_pos, start_y - 2 * line_height, f"ESCOLTA 2: {d.get('ESCOLTA 2', '')}")
        c.drawString(x_pos, start_y - 3 * line_height, f"FIM DA MISSÃO: {fim_missao}")

    def draw_description():
        c.line(2 * cm, height - 18.5 * cm, width - 2 * cm, height - 18.5 * cm)
        c.setFont("Helvetica-Bold", 12)
        c.drawCentredString(width / 2, height - 19.2 * cm, "DETALHAMENTO DA MISSÃO")
        
        styles = getSampleStyleSheet()
        style = styles['BodyText']
        style.fontName = 'Helvetica'
        style.fontSize = 10
        style.leading = 14
        
        descricao_text = d.get('DESCRIÇÃO', 'Nenhuma descrição fornecida.').replace('\n', '  
')
        
        p = Paragraph(f"<b>DESCRIÇÃO:</b> {descricao_text}", style)
        p.wrapOn(c, width - 5 * cm, 10 * cm)
        p.drawOn(c, 2.5 * cm, height - 22 * cm)

    def draw_footer():
        c.setFont("Helvetica", 8)
        text = "TRANSDOURADA NAVEGAÇÃO LTDA 01.259.730/0001-74 ROD BR 316 KM 08, SN AGUA BRANCA 67033-070 ANANINDEUA"
        c.drawCentredString(width / 2, 1.5 * cm, text)

    # --- CHAMADA DAS FUNÇÕES DE DESENHO ---
    draw_header()
    draw_os_details()
    draw_info_section()
    draw_mission_section()
    draw_description()
    draw_footer()
    
    c.save()
    buffer.seek(0)
    return buffer.getvalue()
