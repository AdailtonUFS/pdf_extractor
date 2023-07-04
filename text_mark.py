import io

from PyPDF2 import PdfWriter, PdfReader
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

packet = io.BytesIO()
can = canvas.Canvas(packet, pagesize=letter)
can.drawString(1200, 322, "Marcador")
can.save()

packet.seek(0)

new_pdf = PdfReader(packet)
existing_pdf = PdfReader(open("pdfs/meupdf.pdf", "rb"))

output = PdfWriter()
page = existing_pdf.pages[0]
page.merge_page(new_pdf.pages[0])
output.add_page(page)
output_stream = open("pdfs/pdf_text_mark.pdf", "wb")
output.write(output_stream)
output_stream.close()
