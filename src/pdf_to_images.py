from pdf2image import convert_from_path
from tqdm import tqdm
import os


def generate_pdf_images(filepath: str, image_dir, filename):

    page_image_map = dict()

    pages = convert_from_path(filepath, 500)

    for count, page in enumerate(tqdm(pages, desc=f"Generating image content for {filename}")):
        page_filename = os.path.join(image_dir, f'{filename}_{count}.jpg')
        page.save(page_filename, 'JPEG')
        page_image_map[count] = page_filename

    return page_image_map