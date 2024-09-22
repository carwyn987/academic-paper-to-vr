import argparse
import os
from pypdf import PdfReader

def process_path(file: str) -> dict[int,str]:
    
    assert file[-4:] == ".pdf", "Non-pdf file found"

    page_content_map = dict()
    reader = PdfReader(file)
    assert len(reader.pages) > 0, "No pages acquired"
    for page_num, page_content in enumerate(reader.pages):
        content_str = page_content.extract_text()
        content_str = content_str.replace("\n"," ")
        page_content_map[page_num] = content_str

    return page_content_map    