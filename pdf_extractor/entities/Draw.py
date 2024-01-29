from PyPDF2 import PdfReader
from reportlab.pdfgen import canvas
from tqdm import tqdm

from pdf_extractor.entities.Marker import Marker
from pdf_extractor.entities.PostscriptInstructions import PostscriptInstructions

class Draw:
    def __init__(self, pdf_path, x_coordinate_min=0, x_coordinate_max=0, y_coordinate_min=0, y_coordinate_max=0):
        try:
            self.pdf_path = pdf_path
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

    def process_pdf(self, pdf_path, instruction_func):
        pdf_path = self.validate_path(pdf_path)
        pdf_canvas = self.canvas(pdf_path)
        parser = PostscriptInstructions(pdf_canvas, x_coordinate_min=self.x_coordinate_min,
                                        x_coordinate_max=self.x_coordinate_max, y_coordinate_min=self.y_coordinate_min,
                                        y_coordinate_max=self.y_coordinate_max)
        num_lines = self.count_lines()
        progress_bar = tqdm(total=num_lines, desc='Progresso')

        for pdf_object in self.content:
            indirect_pdf_object = self.reader.get_object(pdf_object)
            data = indirect_pdf_object.get_data()
            postscript_code = data.decode('utf-8')
            postscript_code_lines = postscript_code.split('\n')

            for postscript_code_line in postscript_code_lines:
                instruction_func(parser, postscript_code_line)
                progress_bar.update(1)

        progress_bar.close()

        pdf_canvas.save()

    def complete_pdf(self, pdf_path):
        def process_instruction(parser, postscript_code_line):
            parser.parser_line(postscript_code_line)

        self.process_pdf(pdf_path, process_instruction)

    def line_pdf(self, pdf_path):
        def process_instruction(parser, postscript_code_line):
            if 're' not in postscript_code_line:
                parser.parser_line(postscript_code_line)

        self.process_pdf(pdf_path, process_instruction)

    def count_lines(self):
        num_lines = 0

        for pdf_object in self.content:
            indirect_pdf_object = self.reader.get_object(pdf_object)
            data = indirect_pdf_object.get_data()
            postscript_code = data.decode('utf-8')
            postscript_code_lines = postscript_code.split('\n')

            num_lines += len(postscript_code_lines)

        return num_lines

    def change_color(self, pdf_path):

        pdf_path = self.validate_path(pdf_path)
        pdf_canvas = self.canvas(pdf_path)
        parser = PostscriptInstructions(pdf_canvas, x_coordinate_min=self.x_coordinate_min,
                                        x_coordinate_max=self.x_coordinate_max, y_coordinate_min=self.y_coordinate_min,
                                        y_coordinate_max=self.y_coordinate_max)
        num_lines = self.count_lines()
        progress_bar = tqdm(total=num_lines, desc='Progresso')

        coordinates_x = []
        coordinates_y = []

        for pdf_object in self.content:
            indirect_pdf_object = self.reader.get_object(pdf_object)
            data = indirect_pdf_object.get_data()
            postscript_code = data.decode('utf-8')
            postscript_code_lines = postscript_code.split('\n')

            for line_index, postscript_code_line in enumerate(postscript_code_lines):

                if 'RG' in postscript_code_line or 'rg' in postscript_code_line:
                    if line_index + 1 < len(postscript_code_lines):
                        next_line = postscript_code_lines[line_index + 1]
                        if 'm' in next_line:
                            x, y, *_ = next_line.split(" ")
                            x = float(x)
                            y = float(y)

                            coordinates_x.append(x)
                            coordinates_y.append(y)
                progress_bar.update(1)

        progress_bar.close()
        pdf_canvas.save()

        marker = Marker(self.pdf_path)
        marker.multiple_text_mark('teste.pdf', 0, coordinates_x, coordinates_y)
