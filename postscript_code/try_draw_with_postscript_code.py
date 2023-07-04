from PyPDF2 import PdfReader
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io

output_path = 'resultado.pdf'
c = canvas.Canvas(output_path, pagesize=letter)

pdf_path = '../1-BRSA-313D-AL_perfil_composto.pdf'
temp_pdf_file = io.BytesIO()
c = canvas.Canvas(temp_pdf_file)
reader = PdfReader(pdf_path)

page_num = 0

page = reader.pages[page_num]

content = page['/Contents']

for obj in content:
    indirect_obj = reader.get_object(obj)
    data = indirect_obj.get_data()
    data = data.decode('utf-8')
    lines = data.split('\n')


    for line in lines:
        print(line)
        if line.strip():
            command, *values = line.strip().split()
            if command == 'm':  # instrução move
                x, y = map(float, values)
                c.translate(x, y)

            elif command == 'l': # instrução line
                x, y = map(float, values)
                c.line(0, 0, x, y)

            elif command == 'S': # instrução stroke
                path = c.beginPath()
                c.drawPath(path, stroke=1, fill=0, fillMode=None)

            elif command == 'Q':   # Finaliza o código
                path = c.beginPath()
                c.clipPath(path, stroke=1, fill=0, fillMode=None)

            else:
                pass

    c.save()

