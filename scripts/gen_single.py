from PyPDF2 import PdfFileWriter, PdfFileReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import Color, black
import pandas as pd
import os
import uuid


id = str(uuid.uuid4())
name = "HUNG, YU-CHEN"
dest_dir = "certificates/single"

#%%


name_color = Color(red=(139.0 / 255), green=(20.0 / 255), blue=(22.0 / 255))


def gen_certificate(cert_name, cert_id, dest_dir="certificates"):
    packet = io.BytesIO()
    # create a new PDF with Reportlab
    c = canvas.Canvas(packet, pagesize=letter)

    # NAME
    c.setFillColor(name_color)

    if len(cert_name) <= 20:
        c.setFont("Helvetica", 42)
        c.drawString(3.9 * inch, 5.85 * inch, cert_name)
    else:
        c.setFont("Helvetica", 28)
        c.drawString(3.9 * inch, 5.85 * inch, cert_name)

    pdf_name = dest_dir + os.sep + cert_name.lower().replace(" ", "_") + ".pdf"

    # ID
    c.setFillColor(black)
    c.setFont("Helvetica", 12)
    c.drawString(5.05 * inch, 2.385 * inch, cert_id)

    c.save()

    # move to the beginning of the StringIO buffer
    packet.seek(0)
    new_pdf = PdfFileReader(packet)
    # read your existing PDF
    existing_pdf = PdfFileReader(open("template.pdf", "rb"))
    output = PdfFileWriter()
    # add the "watermark" (which is the new pdf) on the existing page
    page = existing_pdf.getPage(0)
    page.mergePage(new_pdf.getPage(0))
    output.addPage(page)
    # finally, write "output" to a real file
    outputStream = open(pdf_name, "wb")
    output.write(outputStream)
    outputStream.close()


def gen_abv_name(name):
    chunks = name.split(" ")
    last = chunks[-1]
    first_initials = ""
    for chunk in chunks[:-1]:
        first_initials += chunk[0] + ". "
    return first_initials + last


gen_certificate(name, id, dest_dir=dest_dir)
