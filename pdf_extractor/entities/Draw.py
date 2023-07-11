from PyPDF2 import PdfReader
from reportlab.lib.colors import Color
from reportlab.pdfgen import canvas

from pdf_extractor.entities.PostscriptInstructions import PostscriptInstructions


class Draw:
    def __init__(self, pdf_path, x_coordinate_min=0, x_coordinate_max=0, y_coordinate_min=0, y_coordinate_max=0):
        try:
            self.reader: PdfReader = PdfReader(pdf_path)
            page = self.reader.pages[0]
            self.content = page['/Contents']

            self.x_coordinate_min = x_coordinate_min

            if x_coordinate_max == 0:
                self.x_coordinate_max = page.mediabox.width
            else:
                self.x_coordinate_max = x_coordinate_max

            self.y_coordinate_min = y_coordinate_min

            if y_coordinate_max == 0:
                self.y_coordinate_max = page.mediabox.height
            else:
                self.y_coordinate_max = y_coordinate_max

            self.custom_pagesize = (page.mediabox.width, page.mediabox.height)

        except FileNotFoundError:
            print("Arquivo não encontrado! Por favor revise o arquivo e tente novamente")
        except Exception as e:
            print(str(e))

    def canvas(self, pdf_path: str):
        return canvas.Canvas(filename=pdf_path, pagesize=self.custom_pagesize)

    @staticmethod
    def validate_path(pdf_path: str):
        if '.pdf' not in pdf_path:
            pdf_path += '.pdf'

        return pdf_path

    def complete_pdf(self, pdf_path):
        pdf_path = self.validate_path(pdf_path)
        complete_pdf_canvas = self.canvas(pdf_path)
        parser = PostscriptInstructions(complete_pdf_canvas)

        for pdf_object in self.content:
            indirect_pdf_object = self.reader.get_object(pdf_object)
            data = indirect_pdf_object.get_data()
            postscript_code = data.decode('utf-8')
            postscript_code_lines = postscript_code.split('\n')

            for i in range(len(postscript_code_lines)):
                try:
                    if 'rg' in postscript_code_lines[i]:
                        r, g, b, *_ = postscript_code_lines[i].split(" ")
                        color = Color(float(r), float(g), float(b))
                        complete_pdf_canvas.setFillColor(color)

                    if 'm' in postscript_code_lines[i]:
                        x, y, *_ = postscript_code_lines[i].split(" ")
                        x1 = float(x)
                        y1 = float(y)

                        if i + 1 < len(postscript_code_lines):
                            next_line = postscript_code_lines[i + 1]
                            xf, yf, *_ = next_line.split(" ")
                            x2 = float(x)
                            y2 = float(y)
                            if (self.x_coordinate_min < x1 < self.x_coordinate_max) and (
                                    self.y_coordinate_min < y1 < self.y_coordinate_max):
                                complete_pdf_canvas.line(x1, y1, x2, y2)

                    if 're' in postscript_code_lines[i]:
                        x_coord, y_coord, width, height, *_ = postscript_code_lines[i].split(" ")
                        x_coord = float(x_coord)
                        y_coord = float(y_coord)
                        width = float(width)
                        height = float(height)
                        if (self.x_coordinate_min < x_coord < self.x_coordinate_max) and (
                                self.y_coordinate_min < y_coord < self.y_coordinate_max):
                            complete_pdf_canvas.rect(x_coord, y_coord, width, height, fill=True, stroke=False)


                except Exception as e:
                    print("Deu erro na linha", postscript_code_lines[i])
                    print("Deu erro na linha", postscript_code_lines[i + 1].split(" "))
                    print(str(e))

        complete_pdf_canvas.save()

    def line_pdf(self, pdf_path):
        pdf_path = self.validate_path(pdf_path)
        line_pdf = self.canvas(pdf_path)
        parser = PostscriptInstructions(line_pdf)

        for pdf_object in self.content:
            indirect_pdf_object = self.reader.get_object(pdf_object)
            data = indirect_pdf_object.get_data()
            postscript_code = data.decode('utf-8')
            postscript_code_lines = postscript_code.split('\n')

            for i in range(len(postscript_code_lines)):
                try:
                    if 'rg' in postscript_code_lines[i]:
                        r, g, b, *_ = postscript_code_lines[i].split(" ")
                        color = Color(float(r), float(g), float(b))
                        line_pdf.setFillColor(color)

                    if 'm' in postscript_code_lines[i]:
                        x, y, *_ = postscript_code_lines[i].split(" ")
                        x1 = float(x)
                        y1 = float(y)

                        if i + 1 < len(postscript_code_lines):
                            next_line = postscript_code_lines[i + 1]
                            xf, yf, *_ = next_line.split(" ")
                            x2 = float(x)
                            y2 = float(y)

                            if (self.x_coordinate_min < x1 < self.x_coordinate_max) and (
                                    self.y_coordinate_min < y1 < self.y_coordinate_max):
                                line_pdf.line(x1, y1, x2, y2)

                except Exception as e:
                    print("Deu erro na linha", postscript_code_lines[i])
                    print("Deu erro na linha", postscript_code_lines[i + 1].split(" "))
                    print(str(e))
        line_pdf.save()
