from reportlab.lib.colors import Color
from pdf_extractor.entities.Marker import Marker
from pdf_extractor.entities.Rect import Rect

marker = Marker('pdf_extractor/pdfs/pdf_petroleo.pdf')
rect = Rect(100, 313.576, 7.91992, 4.31992)
color = Color(0, 0.498047, 0.24707)
marker.rectangle_mark(rect, color, 'pdf_extractor/pdfs/pdf_petroleo_with_rect_mark.pdf', 0)

# rectangles_transformed = [
#     (4000.94, 313.096, 14.4, 5.03984),
#     (4123.82, 313.096, 6.23984, 4.31992),
#     (4135.34, 313.336, 2.63984, 4.08008),
#     (4140.86, 313.336, 2.88008, 4.08008),
#     (4152.14, 313.096, 2.63984, 4.31992),
#     (4115.66, 313.096, 5.51992, 4.55977),
#     (4124.3, 313.336, 5.76016, 4.08008),
#     (4135.34, 313.576, 2.63984, 3.59961),
#     (4140.62, 313.096, 3.11992, 4.31992),
#     (4152.14, 313.336, 2.88008, 4.31992),
#     (5701.34, 313.336, 19.4398, 4.08008),
#     (5734.46, 313.336, 8.63984, 4.31992),
#     (5748.62, 313.576, 7.91992, 4.31992),
# ]

# packet = io.BytesIO()
# can = canvas.Canvas(packet, pagesize=letter)
#
# for rect in rectangles_transformed:
#     x, y, width, height = rect
#     can.setFillColor(color)
#     can.rect(x, y, width, height, fill=True, stroke=False)
#
# can.save()
#
# packet.seek(0)
