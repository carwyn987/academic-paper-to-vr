from pdf2image import convert_from_path

def pdf_to_images(filepath: str):
    pages = convert_from_path('pdf_file', 500)

    for count, page in enumerate(pages):
        page.save(f'out{count}.jpg', 'JPEG')