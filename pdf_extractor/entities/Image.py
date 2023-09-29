import pdf2image
import pytesseract
from PyPDF2 import PdfReader
from pytesseract import Output

from utils.path import lithologies_file_location


class Image:
    def __init__(self, pdf_path):
        reader = PdfReader(pdf_path)
        self.pdf_path = pdf_path
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

    def search_word(self, word: str):
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

    def get_lithologies_limit(self):
        positions = {'lithology_word_x': 0, 'lithology_word_y': 0, 'profile_word_x': 0, 'profile_word_y': 0}

        lithologies_file = lithologies_file_location()

        with open(lithologies_file, "a+") as file:
            file.seek(0)
            lines = file.readlines()

            if len(lines) > 0:
                for line in lines:
                    filename, lithology_word_x, lithology_word_y, profile_word_x, profile_word_y = line.strip().split(
                        ';;')
                    if filename == self.pdf_path:
                        positions = {'lithology_word_x': float(lithology_word_x),
                                     'lithology_word_y': float(lithology_word_y),
                                     'profile_word_x': float(profile_word_x), 'profile_word_y': float(profile_word_y)}

                        return positions

            lithology_position = self.search_word("litologias:")
            profile_position = self.search_word("perfis")
            if lithology_position and profile_position:
                positions = {'lithology_word_x': lithology_position['x'], 'lithology_word_y': lithology_position['y'],
                             'profile_word_x': profile_position['x'],
                             'profile_word_y': profile_position['y']}

                file.write(self.pdf_path + ";;" + str(lithology_position['x']) + ";;" + str(
                    lithology_position['y']) + ";;" + str(
                    profile_position['x']) + ";;" + str(profile_position['y']) + "\n")

                file.close()

                return positions

        return positions
