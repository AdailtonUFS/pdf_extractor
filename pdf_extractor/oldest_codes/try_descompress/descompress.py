import PyPDF2
import zlib


def descompress_file(file_path):
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)

        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            print(page['/Contents'])
            # lista de IndirectObject(8, 0, 140555085463504)
            for item in page['/Contents']:
                if isinstance(item, PyPDF2.generic.IndirectObject):
                    indirect_obj = reader.get_object(item)
                    if '/Filter' in indirect_obj and indirect_obj['/Filter'] == '/FlateDecode':
                        decompressed_content = zlib.decompress(indirect_obj.get_data())

                        print(decompressed_content)
                    else:
                        print(indirect_obj)


pdf_path = 'altere o path para o pdf'

descompress_file(pdf_path)
