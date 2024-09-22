import argparse
import os

from src.process_raw_pdf import process_path

def main(args):

    path = args.path
    if os.path.isfile(path):
        files = [path]
    elif os.path.isdir(path):
        files = [os.path.join(path, file) for file in os.listdir(path) if os.path.isfile(os.path.join(path, file))]
    else:
        print(f"Error: {path} is neither a file nor a directory")
    assert len(files) > 0, "No files found."

    for file in files:
        page_content_map = process_path(file)
        print(page_content_map)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate video from a pdf')
    parser.add_argument('path', help='path to a file or directory')
    args = parser.parse_args()
    main(args)