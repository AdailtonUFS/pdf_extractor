from PyPDF2 import PdfReader
from reportlab.pdfgen import canvas
from reportlab.lib.colors import Color
from reportlab.lib.pagesizes import inch

custom_width = 130.59722222222223  # em polegadas
custom_height = 13.01388888888889  # em polegadas

custom_pagesize = (custom_width * inch, custom_height * inch)

pdf_lines_draw = 'pdf_lines_draw.pdf'
pdf_with_rect_draw = 'pdf_with_rect_draw.pdf'
c = canvas.Canvas(pdf_lines_draw, pagesize=custom_pagesize)
complete_canvas = canvas.Canvas(pdf_with_rect_draw, pagesize=custom_pagesize)

pdf_path = '../../pdfs/meupdf.pdf'
reader = PdfReader(pdf_path)
page = reader.pages[0]

content = page['/Contents']

for obj in content:
    indirect_obj = reader.get_object(obj)
    data = indirect_obj.get_data()
    data = data.decode('utf-8')
    lines = data.split('\n')

    for i in range(len(lines)):
        try:
            if 'm' in lines[i]:
                x, y, *_ = lines[i].split(" ")
                x1 = float(x)
                y1 = float(y)

                if i + 1 < len(lines):
                    next_line = lines[i + 1]
                    xf, yf, *_ = next_line.split(" ")
                    x2 = float(x)
                    y2 = float(y)

                    c.line(x1, y1, x2, y2)
                    complete_canvas.line(x1, y1, x2, y2)


        except Exception as e:
            print("Deu erro na linha", lines[i])
            print("Deu erro na linha", lines[i+1].split(" "))
            print(str(e))


for obj in content:
    indirect_obj = reader.get_object(obj)
    data = indirect_obj.get_data()
    data = data.decode('utf-8')
    lines = data.split('\n')

    start = 0
    for i in range(len(lines)):
        try:
            if 'rg' in lines[i]:
                r,g,b, *_ = lines[i].split(" ")
                color = Color(float(r), float(g), float(b))
                complete_canvas.setFillColor(color)

            if 're' in lines[i]:
                x_coord, y_coord, width, height, *_ = lines[i].split(" ")
                x_coord = float(x_coord)
                y_coord = float(y_coord)
                width = float(width)
                height = float(height)

                complete_canvas.rect(x_coord, y_coord, width, height, fill=True, stroke=False)

        except Exception as e:
            print("Deu erro na linha", lines[i])
            print("Deu erro na linha", lines[i+1].split(" "))
            print(str(e))

c.save()
complete_canvas.save()
