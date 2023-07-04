import subprocess
import shutil
import platform
import sys


class Ghostscript:
    def __init__(self):
        self.gs_path = Ghostscript.get_ghostscript_path()
        print(self.gs_path)

    def ps_to_pdf(self, postscript_input_file_path: str, pdf_output_file_path: str):
        command = [self.gs_path, "-sDEVICE=pdfwrite", "-o=" + pdf_output_file_path, "-dNOPAUSE", "-dBATCH",
                   postscript_input_file_path]

        try:
            subprocess.run(command)
        except Exception as e:
            print(str(e))

    def pdf_to_ps(self, pdf_input_file_path: str, postscript_output_file_path: str):
        command = [self.gs_path, "-sDEVICE=ps2write", "-o=" + postscript_output_file_path, pdf_input_file_path]

        try:
            subprocess.run(command)
        except Exception as e:
            print(str(e))

    @staticmethod
    def get_ghostscript_path():
        my_os = platform.system()

        win64 = sys.maxsize > 2 ** 32
        windows_ghostscript = 'gswin64' if win64 == "Linux" else 'gswin32'

        program = 'gs' if my_os == "Linux" else windows_ghostscript

        gs_path = shutil.which(program)
        if gs_path is None:
            raise Exception("Ghostscript not found, please check if is installed and check environment variables")

        return gs_path
