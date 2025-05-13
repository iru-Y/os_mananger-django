import os
from io import BytesIO
from decimal import Decimal, InvalidOperation

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from django.conf import settings

def generate_os_pdf(customer):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    w, h = A4

    styles = getSampleStyleSheet()
    normal = styles['Normal']
    normal.fontName = 'Helvetica'
    normal.fontSize = 10
    bold = ParagraphStyle('bold', parent=normal, fontName='Helvetica-Bold')
    red = ParagraphStyle('red', parent=normal, textColor=colors.red, fontName='Helvetica-Bold')

    c.setFont("Helvetica-Bold", 18)
    c.drawString(20*mm, h-20*mm, "[Logo]")
    c.drawString(55*mm, h-20*mm, "JamesCell - Assistência Técnica")
    c.setFont("Helvetica", 9)
    c.drawString(55*mm, h-25*mm, "99 8443-7903 | 99 991542276 | Mercado da rodoviária box 27")

    c.setStrokeColor(colors.grey)
    c.setLineWidth(0.5)
    c.line(20*mm, h-30*mm, w-20*mm, h-30*mm)

    y = h - 36*mm
    client_data = [
        ['Nome Completo:', customer.full_name],
        ['E-mail:',         customer.email],
        ['Telefone:',       customer.phone],
        ['Descrição do Serviço:', customer.description],
    ]
    table = Table(client_data, colWidths=[45*mm, 120*mm])
    table.setStyle(TableStyle([
        ('FONTNAME',   (0,0), (-1,-1), 'Helvetica'),
        ('FONTSIZE',   (0,0), (-1,-1), 10),
        ('LINEBELOW',  (1,0),(1,0),     0.25, colors.gray),
        ('LINEBELOW',  (1,1),(1,1),     0.25, colors.gray),
        ('LINEBELOW',  (1,2),(1,2),     0.25, colors.gray),
        ('BACKGROUND', (0,3),(1,3),     colors.whitesmoke),
    ]))
    w_table, h_table = table.wrapOn(c, w, h)
    table.drawOn(c, 20*mm, y - h_table)

    y = y - h_table - 10*mm

    try:
        service_val = Decimal(customer.service_price)
        service_str = f"R$ {service_val:,.2f}"
    except (InvalidOperation, TypeError):
        service_str = f"R$ {customer.service_price}"

    tech_data = [
        ['Número da OS', 'Data de Fechamento', 'Preço Total'],
        [
            str(customer.id),
            customer.created_at.strftime("%d/%m/%Y"),
            service_str,
        ],
    ]
    t2 = Table(tech_data, colWidths=[50*mm, 50*mm, 50*mm])
    t2.setStyle(TableStyle([
        ('GRID',       (0,0), (-1,-1),       0.5, colors.black),
        ('BACKGROUND', (0,0),(-1,0),         colors.lightgrey),
        ('ALIGN',      (2,1),(2,1),         'RIGHT'),
        ('TEXTCOLOR',  (2,1),(2,1),         colors.red),
        ('FONTNAME',   (0,0),(-1,0),        'Helvetica-Bold'),
    ]))
    w2, h2 = t2.wrapOn(c, w, h)
    t2.drawOn(c, 20*mm, y - h2)

    y = y - h2 - 15*mm

    approval_data = [
        ['Responsável Técnico:',    '_______________________________'],
        ['Assinatura do Cliente:',  '_______________________________'],
        ['Cláusulas:', 
         '1. Garantia de 30 dias para serviços prestados, conforme Código de Defesa do \nConsumidor.'],
        ['', 
         '2. A garantia cobre apenas os serviços realizados e não abrange danos causados \npor mau uso ou outros fatores externos.'],
        ['', 
         '3. A senha de desbloqueio fornecida será utilizada exclusivamente para os \ntestes técnicos e será removida após a conclusão do serviço.']
    ]
    t3 = Table(approval_data, colWidths=[50*mm, 120*mm])
    t3.setStyle(TableStyle([
        ('FONTNAME',    (0, 0), (-1, -1),  'Helvetica'),
        ('FONTSIZE',    (0, 0), (-1, -1),  10),
        ('TOPPADDING',  (0, 0), (-1, -1),  5),
        ('BOTTOMPADDING',(0, 0), (-1, -1), 25),
        ('LEFTPADDING', (0, 0), (-1, -1),  2),
        ('RIGHTPADDING',(0, 0), (-1, -1),  2),
    ]))
    w3, h3 = t3.wrapOn(c, w, h)
    t3.drawOn(c, 20*mm, y - h3 - 25*mm)

    dot_start_x = w - 20*mm - 40*mm
    dot_y = y + 5*mm
    c.setFont("Helvetica-Bold", 10)
    c.drawString(dot_start_x - 60*mm, dot_y - 3*mm, "Senha de Bloqueio:")
    for row in range(3):
        for col in range(3):
            cx = dot_start_x + col * 8 * mm
            cy = dot_y - row * 8 * mm
            c.circle(cx, cy, 2*mm, stroke=1, fill=0)
    c.setFont("Helvetica", 8)
    c.drawString(dot_start_x - 60*mm, dot_y + 1*mm, 
                 "Informe a senha de desbloqueio do celular")

    y_footer = 20*mm
    c.setFont("Helvetica", 6)
    c.drawString(20*mm, y_footer + 10*mm, 
                 "Tratamento da Liga: seguir as normas de assistência técnica conforme regulamentação vigente.")
    c.drawString(20*mm, y_footer + 5*mm, 
                 "Garantia dos serviços executados: 30 dias, contados a partir da data de conclusão.")

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer
