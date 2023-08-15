import pdf2image
import pytesseract
from pytesseract import Output, TesseractError

from pdf_extractor.entities.Marker import Marker

pdf_path = "pdf_aqui"

images = pdf2image.convert_from_path(pdf_path)
pil_im = images[0]

ocr_dict: dict = pytesseract.image_to_data(pil_im, output_type=Output.DICT)
word_pos = {}
print(ocr_dict.keys())
if len(ocr_dict['text']) == len(ocr_dict['top']) == len(ocr_dict['left']):
    i: int = 0
    while i < len(ocr_dict['text']):
        if ocr_dict['text'][i].lower() == "litologias:":
            word_pos['word'] = ocr_dict['text'][i].lower()
            word_pos['x'] = ocr_dict['left'][i]
            word_pos['y'] = ocr_dict['top'][i]

        i += 1
pontos = {'x': word_pos['x'] * 0.75, 'y': word_pos['y'] * 0.75}
polegadas = {'x': word_pos['x'] / 96, 'y': word_pos['y'] / 96}

marker = Marker(pdf_path)
marker.text_mark('teste2.pdf', 0, "normal", word_pos['x'], word_pos['y'])
marker.text_mark('teste2.pdf', 0, "pontos", pontos['x'], pontos['y'])
marker.text_mark('teste2.pdf', 0, "polegadas", polegadas['x'], polegadas['y'])
# print(word_pos)
