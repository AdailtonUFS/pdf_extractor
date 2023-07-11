from pdf_extractor.entities.Draw import Draw

pdf_file_path = input("PDF FILE PATH (INPUT) \n")
option = input("Escolha a opção: \n 1- Gerar PDF com as linhas \n 2- Gerar PDF com os retângulos \n 0- Sair \n")
option = int(option)

while option != 0:
    if option == 1:
        path = input("Informe o caminho onde o arquivo será salvo:\n")
        coordinates = input(
            "Deseja limitar a area do pdf?"
            "\n Caso sim: digite as coordenadas separadas por \",\""
            "\n xmin: \"Posição onde o arquivo começará a ser escrito no eixo x"
            "\n xmin: \"Posição onde o arquivo terminará a ser escrito no eixo x"
            "\n ymin: \"Posição onde o arquivo começará a ser escrito no eixo y"
            "\n ymax: \"Posição onde o arquivo terminará a ser escrito no eixo y"
            "\n Exemplo 1230,8900,120,480"
            "\n Caso não: Apenas deixe em branco\n"
        )

        if len(coordinates.split(',')) == 4:
            x_min, x_max, y_min, y_max = coordinates.split(',')
            x_min = float(x_min)
            x_max = float(x_max)
            y_min = float(y_min)
            y_max = float(y_max)

            draw = Draw(pdf_file_path, x_min, x_max, y_min, y_max)
        else:
            draw = Draw(pdf_file_path)

        draw.line_pdf(path)
    if option == 2:
        path = input("Informe o caminho onde o arquivo será salvo:\n")
        coordinates = input(
            "Deseja limitar a area do pdf?"
            "\n Caso sim: digite as coordenadas separadas por \",\""
            "\n xmin: \"Posição onde o arquivo começará a ser escrito no eixo x"
            "\n xmin: \"Posição onde o arquivo terminará a ser escrito no eixo x"
            "\n ymin: \"Posição onde o arquivo começará a ser escrito no eixo y"
            "\n ymax: \"Posição onde o arquivo terminará a ser escrito no eixo y"
            "\n Exemplo 1230,8900,120,480"
            "\n Caso não: Apenas deixe em branco\n"
        )

        if len(coordinates.split(',')) == 4:
            x_min, x_max, y_min, y_max = coordinates.split(',')
            x_min = float(x_min)
            x_max = float(x_max)
            y_min = float(y_min)
            y_max = float(y_max)

            draw = Draw(pdf_file_path, x_min, x_max, y_min, y_max)
        else:
            draw = Draw(pdf_file_path)
        draw.complete_pdf(path)

    option = input("Escolha a opção: \n 1- Gerar PDF com as linhas \n 2- Gerar PDF com os retângulos \n 0- Sair \n")
    option = int(option)

