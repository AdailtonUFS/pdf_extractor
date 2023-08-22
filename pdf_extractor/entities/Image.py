import pdf2image
import pytesseract
from PyPDF2 import PdfReader
from pytesseract import Output


class Image:
    def __init__(self, pdf_path):
        reader = PdfReader(pdf_path)
        self.page = reader.pages[0]

        images = pdf2image.convert_from_path(pdf_path)
        self.image = images[0]

    def _all_words(self):
        ocr_dict: dict = pytesseract.image_to_data(self.image, output_type=Output.DICT)
        return ocr_dict

    def _convert_pixels_to_pdf(self, word_position):
        pixel_to_point_width_ratio = float(self.page.mediabox.width / self.image.width)
        pixel_to_point_height_ratio = float(self.page.mediabox.height / self.image.height)
        x_converted_coordinate = word_position['x'] * pixel_to_point_width_ratio
        y_converted_coordinate = float(self.page.mediabox.height) - (word_position['y'] * pixel_to_point_height_ratio)
        return {'x': x_converted_coordinate, 'y': y_converted_coordinate}

    def search_word_in_words_collection(self, word: str):
        words_collection = self._all_words()

        word_position = {}
        i: int = 0
        while i < len(words_collection['text']):
            if words_collection['text'][i].lower() == word:
                word_position['word'] = words_collection['text'][i].lower()
                word_position['x'] = words_collection['left'][i]
                word_position['y'] = words_collection['top'][i]

                break

            i += 1
        if not word_position:
            raise Exception("Ocorreu um erro ao buscar as palavras")

        return self._convert_pixels_to_pdf(word_position)
