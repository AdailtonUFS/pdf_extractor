import io

from PyPDF2 import PdfWriter, PdfReader
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.colors import Color

from pdf_extractor.entities.Rect import Rect


class Marker:
    def __init__(self, pdf_file_path: str):
        self.pdf = PdfReader(open(pdf_file_path, "rb"))

    def text_mark(self, output_file_pdf_path: str, page_number: int, marker_text, coordinate_x, coordinate_y):
        packet = Marker.text_draw(marker_text, coordinate_x, coordinate_y)
        marker_pdf = PdfReader(packet)
        page_to_draw = self.pdf.pages[page_number]
        page_to_draw.merge_page(marker_pdf.pages[0])
        Marker.generate_marker_pdf(page_to_draw, output_file_pdf_path)

    def rectangle_mark(self, rect: Rect, color: Color, output_file_pdf_path: str, page_number: int):
        packet = Marker.rect_draw(rect, color)
        marker_pdf = PdfReader(packet)
        page_to_draw = self.pdf.pages[page_number]
        page_to_draw.merge_page(marker_pdf.pages[0])
        Marker.generate_marker_pdf(page_to_draw, output_file_pdf_path)

    @staticmethod
    def text_draw(text: str, coordinate_x, coordinate_y):
        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=letter)
        can.drawString(coordinate_x, coordinate_y, text)
        can.save()
        packet.seek(0)

        return packet

    @staticmethod
    def rect_draw(rect: Rect, color: Color):
        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=letter)
        can.setFillColor(color)
        can.rect(rect.x, rect.y, rect.width, rect.height, fill=True, stroke=False)
        can.save()
        packet.seek(0)

        return packet

    @staticmethod
    def generate_marker_pdf(page_to_draw, output_file_pdf_path: str):
        pdf_generated = PdfWriter()
        pdf_generated.add_page(page_to_draw)

        file_pdf = open(output_file_pdf_path, "wb")
        pdf_generated.write(file_pdf)
        file_pdf.close()
