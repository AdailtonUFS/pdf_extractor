from pdf_extractor.entities.Draw import Draw
from pdf_extractor.entities.Image import Image
from utils.litologies import lithology_rect
from utils.path import path_to_pdf_generated

pdf_file_path = input("PDF FILE PATH (INPUT) \n")
pdf_to_save_file = path_to_pdf_generated(pdf_file_path)
image = Image(pdf_file_path)
positions = image.get_lithologies_limit()

draw = Draw(pdf_file_path, y_coordinate_min=positions['profile_word_y'], y_coordinate_max=positions['lithology_word_y'])
draw.complete_pdf(pdf_to_save_file)

lithology_rect(pdf_to_save_file)

# # /home/skywalker/projects/python/pdfquery/pdf_extractor/pdfs/3CP1853SE_PC.pdf
