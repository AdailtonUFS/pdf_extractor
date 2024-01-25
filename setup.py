from pdf_extractor.entities.Draw import Draw
from pdf_extractor.entities.Image import Image
from utils.litologies import lithology_rect
from utils.path import path_to_pdf_generated

pdf_input_path = input("Aponte o caminho total para o seu pdf \n")

pdf_output_path = path_to_pdf_generated(pdf_input_path)
image = Image(pdf_input_path)
positions = image.get_lithologies_limit()

draw = Draw(pdf_input_path, y_coordinate_min=positions['profile_word_y'], y_coordinate_max=positions['lithology_word_y'])
draw.change_color(pdf_output_path)

# lithology_rect(pdf_output_path)

# /home/skywalker/projects/UFS/python/smart_litol/pdf_extractor/pdfs/brsa.pdf