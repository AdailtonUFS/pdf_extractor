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

position = {'x': 0, 'y': 0 , 'perf_x': 0, 'perf_y': 0}
exists = False
with open('litogias_location.txt', "a+") as file:
    file.seek(0)
    lines = file.readlines()

    if len(lines) > 0:
        for line in lines:
            file_name, x, y, perfis_x, perfis_y = line.strip().split(';;')
            if file_name == pdf_file_path:
                position = {'x': float(x), 'y': float(y), 'perf_x': float(perfis_x), 'perf_y': float(perfis_y)}
                exists = True
                break

    if not exists:
        image = Image(pdf_file_path)
        position_lit = image.search_word("litologias:")
        perfis = image.search_word("perfis")
        position = {'x': position_lit['x'], 'y': position_lit['y'], 'perf_x': perfis['x'], 'perf_y': perfis['y']}
        file.write(pdf_file_path + ";;" + str(position['x']) + ";;" + str(position['y']) + ";;" + str(perfis['x']) + ";;" + str(perfis['y']) + "\n")


file.close()
print(position)
draw = Draw(pdf_file_path, y_coordinate_min=position['perf_y'], y_coordinate_max=position['y'])
draw.complete_pdf(path_save)

