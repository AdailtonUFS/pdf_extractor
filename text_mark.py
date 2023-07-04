from pdf_extractor.entities.Marker import Marker

marker = Marker('pdf_extractor/pdfs/pdf_petroleo.pdf')
marker.text_mark('pdf_extractor/pdfs/pdf_petroleo_with_text_mark.pdf', 0, "Marcador", 1200, 322)
marker.text_mark('pdf_extractor/pdfs/pdf_petroleo_with_text_mark.pdf', 0, "Marcador", 100, 322)
marker.text_mark('pdf_extractor/pdfs/pdf_petroleo_with_text_mark1.pdf', 0, "Marcador", 100, 322)
