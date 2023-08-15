import subprocess
import platform


def open_pdf(pdf_path):
    my_os = platform.system()
    if my_os == "Linux":
        subprocess.run(['xdg-open', pdf_path])
    elif my_os == "Windows":
        subprocess.run(['start', pdf_path], shell=True)
    elif my_os == "Darwin":
        subprocess.run(['open', pdf_path])
    else:
        print("Sistema operacional não suportado.")
