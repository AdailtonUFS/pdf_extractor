import subprocess

postscript_file = "output.ps"
ghostscript_path = "change_to_ghostscript_path"
command = [ghostscript_path, "-sDEVICE=pdfwrite", "-o=pdf_generated.pdf", "-dNOPAUSE", "-dBATCH", postscript_file]
subprocess.run(command)

print("PDF gerado com sucesso: pdf_generated.pdf")
