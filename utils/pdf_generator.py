import os
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from django.conf import settings 

def generate_os_pdf(customer):
  
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    w, h = A4

    header_y = h - 20*mm
    c.setFont("Helvetica-Bold", 24)
    c.drawCentredString(w/2, header_y, "ASSISTÊNCIA CELULAR")

    logos = [
        ('samsung.png',   20*mm),
        ('motorola.png',  50*mm),
        ('lg.png',        80*mm),
        ('xiaomi.png',   110*mm),
    ]
    for filename, x in logos:
        path = os.path.join(settings.STATIC_ROOT, 'logos', filename)
        if os.path.exists(path):
            c.drawImage(path, x, header_y-15*mm, width=20*mm, height=10*mm, preserveAspectRatio=True)

    c.setFont("Helvetica", 10)
    c.drawString(20*mm, header_y-25*mm, "Rua seu endereço:")

    y = header_y - 35*mm
    c.setFont("Helvetica", 10)
    c.drawString(20*mm, y, "Data: ________/________/________")
    c.drawString(80*mm, y, f"Cliente: {customer.full_name}")
    c.drawString(150*mm, y, f"Cel: {customer.phone}")

    y -= 7*mm
    c.drawString(20*mm, y, f"CPF: {customer.cpf if hasattr(customer, 'cpf') else '___________'}")
    c.drawString(80*mm, y, f"E-mail: {customer.email}")

    y -= 15*mm
    c.setFont("Helvetica-Bold", 12)
    c.drawString(20*mm, y, "DESCRIÇÃO DO EQUIPAMENTO")
    c.setFont("Helvetica", 10)

    y -= 7*mm
    c.drawString(20*mm, y, f"Aparelho: {getattr(customer, 'aparelho', '________________')}")
    y -= 7*mm
    c.drawString(20*mm, y, "Marca:")
    c.drawString(40*mm, y, getattr(customer, 'marca', '________'))
    c.drawString(80*mm, y, "Mod:")
    c.drawString(95*mm, y, getattr(customer, 'modelo', '________'))
    y -= 7*mm
    c.drawString(20*mm, y, "IMEI:")
    c.drawString(35*mm, y, getattr(customer, 'imei', '________________'))

    y -= 15*mm
    c.setFont("Helvetica-Bold", 12)
    c.drawString(20*mm, y, "LAUDO TÉCNICO")
    c.drawString(110*mm, y, "SENHA")
    c.setFont("Helvetica", 10)
    c.rect(20*mm, y-25*mm, 120*mm, 25*mm, stroke=1, fill=0)
    for i in range(6):
        cx = 115*mm + i*6*mm
        cy = y - 12*mm
        c.circle(cx, cy, 2*mm, stroke=1, fill=0)

    y -= 35*mm
    c.setFont("Helvetica-Bold", 10)
    c.drawString(20*mm, y, "TOTAL R$:")
    c.rect(35*mm, y-3*mm, 40*mm, 7*mm, stroke=1, fill=0)
    c.drawString(80*mm, y, "Garantia de ___ dias")

    y -= 15*mm
    c.setFont("Helvetica-Bold", 10)
    c.drawString(20*mm, y, "QNT")
    c.drawString(40*mm, y, "DESCRIÇÃO DOS PRODUTOS")
    c.drawString(140*mm, y, "VALOR R$")

    for i in range(6):
        yy = y - 5*mm - i*7*mm
        c.line(20*mm, yy, 190*mm, yy)

    y = yy - 15*mm
    c.setFont("Helvetica", 10)
    c.drawString(20*mm, y, "☐ Dinheiro    ☐ Crédito    ☐ Débito")
    c.drawString(110*mm, y, "TOTAL R$ ________")

    y -= 10*mm
    c.drawString(20*mm, y, "Ass. Cliente: ________________________________")

    y -= 10*mm
    c.setFont("Helvetica", 6)
    c.drawString(20*mm, y, "1- A GARANTIA dos serviços executados é de 60 (sessenta) dias ...")
    c.drawString(20*mm, y-4*mm, "2- A não retirada ...")
    c.drawString(20*mm, y-8*mm, "3- Os equipamentos ...")

    c.showPage()
    c.save()

    buffer.seek(0)
    return buffer
