import PyPDF2

pdf_file = '../pdfs/meupdf.pdf'

with open(pdf_file, 'rb') as file:
    pdf_reader = PyPDF2.PdfReader(file)
    page = pdf_reader.pages[0]

    width = page.mediabox.width
    height = page.mediabox.height

    width_inches = width / 72
    height_inches = height / 72

    print('Largura:', width, 'pontos', 'ou', width_inches, 'polegadas')
    print('Altura:', height, 'pontos', 'ou', height_inches, 'polegadas')
