import argparse
import subprocess
import os

from src.process_raw_pdf import process_path
from src.clean_text import clean_page_content_map
from src.text_to_audio import generate_audio
from src.pdf_to_images import generate_pdf_images
from src.stitcher import stitch_pages

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

        filename = os.path.splitext(os.path.basename(file))[0]
        base_dir = os.path.join(args.bin_dir, filename)
        audio_dir = os.path.join(base_dir, "audio")
        image_dir = os.path.join(base_dir, "images")
        output_file = os.path.join(base_dir,f"{filename}.mp4")
        os.makedirs(base_dir, exist_ok=True)
        os.makedirs(audio_dir, exist_ok=True)
        os.makedirs(image_dir, exist_ok=True)

        page_content_map = process_path(file)
        cleaned_page_content_map = clean_page_content_map(filename, page_content_map, args.model)
        
        if args.verbose:
            print("Pre-cleaned:::: \n ===========================================\n" + page_content_map[0])
            print("\n\nPost-cleaned:::: \n ===========================================\n" + cleaned_page_content_map[0])

        page_audio_map = generate_audio(audio_dir, filename, cleaned_page_content_map, args.voice)
        print(page_audio_map)

        # For testing, at this point we have dictionaries of the text, cleaned text, audio paths
        # page_audio_map = {
        #     0: "bin/a_formal_measure_of_machine_intelligence/audio/a_formal_measure_of_machine_intelligence_0.mp3",
        #     1: "bin/a_formal_measure_of_machine_intelligence/audio/a_formal_measure_of_machine_intelligence_1.mp3",
        #     2: "bin/a_formal_measure_of_machine_intelligence/audio/a_formal_measure_of_machine_intelligence_2.mp3",
        #     3: "bin/a_formal_measure_of_machine_intelligence/audio/a_formal_measure_of_machine_intelligence_3.mp3",
        #     4: "bin/a_formal_measure_of_machine_intelligence/audio/a_formal_measure_of_machine_intelligence_4.mp3",
        #     5: "bin/a_formal_measure_of_machine_intelligence/audio/a_formal_measure_of_machine_intelligence_4.mp3",
        #     6: "bin/a_formal_measure_of_machine_intelligence/audio/a_formal_measure_of_machine_intelligence_4.mp3",
        #     7: "bin/a_formal_measure_of_machine_intelligence/audio/a_formal_measure_of_machine_intelligence_4.mp3",
        # }

        # Get image dictionary
        page_image_map = generate_pdf_images(file, image_dir, filename)

        stitch_pages(page_image_map, page_audio_map, output_file, args.fps)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate video from a pdf')
    parser.add_argument('path', help='Path to a file or directory')
    parser.add_argument('--bin_dir', default="bin", help='Output directory')
    parser.add_argument('--voice', default="onyx", choices=["alloy", "echo", "fable", "onyx", "nova", "shimmer"], help='Voice profile to use')
    parser.add_argument('--verbose', action='store_true', help='Print example outs')
    parser.add_argument('--fps', default=1, help='Choose video fps. Note: despite repetitive frames throughout the video, this has an enormous impact on compilation speed.')
    parser.add_argument('--model', default='gpt-3.5-turbo', choices=['gpt-3.5-turbo', "gpt-4o-mini"])
    args = parser.parse_args()

    main(args)