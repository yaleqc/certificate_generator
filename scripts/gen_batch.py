from PyPDF2 import PdfFileWriter, PdfFileReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import Color, black
import pandas as pd
import os


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


tot_abv_names = []
tot_cert_ids = []
gen_pdfs = False

# accents

data_file = "data/accents.csv"
dest_dir = "certificates/accents"

df = pd.read_csv(data_file, encoding="utf-8")
for i in range(len(df["name"])):
    cert_name = df["name"][i]
    cert_id = df["id"][i]
    if gen_pdfs:
        gen_certificate(cert_name, cert_id, dest_dir=dest_dir)

    tot_abv_names.append(gen_abv_name(df["name"][i]))
    tot_cert_ids.append(cert_id)


# normal

data_file = "data/normal.csv"
dest_dir = "certificates/normal"

df = pd.read_csv(data_file, encoding="utf-8")
for i in range(len(df["name"])):
    cert_name = df["name"][i]
    cert_id = df["id"][i]
    if gen_pdfs:
        gen_certificate(cert_name, cert_id, dest_dir=dest_dir)

    tot_abv_names.append(gen_abv_name(df["name"][i]))
    tot_cert_ids.append(cert_id)

# export to csv
import csv

with open("verification.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerows(zip(tot_abv_names, tot_cert_ids))
