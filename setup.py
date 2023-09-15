import os

from pdf_extractor.entities.Draw import Draw
from pdf_extractor.entities.Image import Image
from utils.uniquify_file import uniquify

def define_pdf_path():
    pdf_file_path = input("PDF FILE PATH (INPUT) \n")

    path_array = pdf_file_path.split('/')

    filename = path_array[len(path_array) - 1]
    folder_name = filename.replace('.pdf', '')

    path_folder = '/home/skywalker/projects/python/pdfquery/pdf_extractor/pdfs/generated/' + folder_name

    if not os.path.exists(path_folder):
        os.mkdir(path_folder)


    path_save = uniquify(path_folder + "/" + filename)
    return [pdf_file_path, path_save]


pdf_file_path, path_save = define_pdf_path()


image = Image(pdf_file_path)
position = image.search_word("litologias:")
draw = Draw(pdf_file_path, y_coordinate_min=position['y'], x_coordinate_min=position['x'])
draw.complete_pdf(path_save)


