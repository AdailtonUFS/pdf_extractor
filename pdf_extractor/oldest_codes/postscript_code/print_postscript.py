from PyPDF2 import PdfReader

pdf_path = 'path do pdf aqui'

reader = PdfReader(pdf_path)
page = reader.pages[0]

content = page['/Contents']

for obj in content:
    indirect_obj = reader.get_object(obj)
    data = indirect_obj.get_data()
    print(data)
