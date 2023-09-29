import os

ROOT_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

PDFS_DIR = ROOT_DIR + "/pdf_extractor/pdfs"

PDFS_GENERATED_DIR = ROOT_DIR + "/pdf_extractor/pdfs/generated"