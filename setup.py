from pdf_extractor.entities.Ghostscript import Ghostscript

pdf_file_path = input("PDF FILE PATH (INPUT) \n")
ps_file_path = input("POSTSCRIPT FILE PATH (OUTPUT) \n")

ghostscript = Ghostscript()
ghostscript.pdf_to_ps(pdf_file_path, ps_file_path)
