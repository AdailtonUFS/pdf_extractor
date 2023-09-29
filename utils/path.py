import os

from utils.uniquify_file import uniquify
from pdf_extractor import constants

def validate_folders():
    if not os.path.exists(constants.PDFS_DIR):
        os.mkdir(constants.PDFS_DIR)

    if not os.path.exists(constants.PDFS_GENERATED_DIR):
        os.mkdir(constants.PDFS_GENERATED_DIR)

def path_to_lithologies_generated(pdf_file_path: str) -> str:
    validate_folders()

    path_array = pdf_file_path.split('/')

    filename = path_array[len(path_array) - 1]

    folder_name = filename.replace('.pdf', '')

    if not os.path.exists(constants.PDFS_GENERATED_DIR + "/" + folder_name):
        os.mkdir(constants.PDFS_GENERATED_DIR + "/" + folder_name)

    lithologies_generated_folder = constants.PDFS_GENERATED_DIR + "/" + folder_name + "/lithologies/"

    if not os.path.exists(lithologies_generated_folder):
        os.mkdir(lithologies_generated_folder)

    path_file_lithologies = lithologies_generated_folder + filename

    return path_file_lithologies


def path_to_pdf_generated(pdf_file_path: str):
    validate_folders()

    path_array = pdf_file_path.split('/')

    filename = path_array[len(path_array) - 1]

    folder_name = filename.replace('.pdf', '')

    if not os.path.exists(constants.PDFS_GENERATED_DIR + "/" + folder_name):
        os.mkdir(constants.PDFS_GENERATED_DIR + "/" + folder_name)

    path_folder = constants.PDFS_GENERATED_DIR + "/" + folder_name + "/pdfs"

    if not os.path.exists(path_folder):
        os.mkdir(path_folder)

    path_save = uniquify(path_folder + "/" + filename)
    return path_save


def lithologies_file_location() -> str:
    return constants.ROOT_DIR + "/lithologies_localization.txt"
