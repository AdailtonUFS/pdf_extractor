import PyPDF2

# Caminho para o arquivo PDF
pdf_file = '=output.pdf'

# Abra o arquivo PDF em modo leitura binária
with open(pdf_file, 'rb') as file:
    # Crie um objeto PDFReader do PyPDF2
    pdf_reader = PyPDF2.PdfReader(file)

    # Obtenha o objeto da primeira página do PDF
    page = pdf_reader.pages[0]

    # Obtenha a largura e altura da página em pontos (1 ponto = 1/72 polegadas)
    width = page.mediabox.width
    height = page.mediabox.height

    # Converta a largura e altura para outras unidades, se necessário
    width_inches = width / 72
    height_inches = height / 72

    # Imprima as dimensões da página
    print('Largura:', width, 'pontos', 'ou', width_inches, 'polegadas')
    print('Altura:', height, 'pontos', 'ou', height_inches, 'polegadas')
