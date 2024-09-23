from pathlib import Path
from openai import OpenAI
from tqdm import tqdm
import os
import nltk
from nltk.tokenize import sent_tokenize
nltk.download('punkt_tab')

def generate_audio(audio_dir: str, filename: str, cleaned_page_content_map: dict[int,str], voice: str) -> dict[int,list]:

    page_audio_map = dict()

    for page, content in tqdm(cleaned_page_content_map.items(), desc=f"Generating audio for {filename}"):
        #page_audio_map[page] = text_to_audio(audio_dir, filename, page, content, voice)

        if os.path.exists(os.path.join(audio_dir, f"{filename}_{page}.mp3")):
            print("Skipping audio transcription, already exists ...")
            page_audio_map[page] = [os.path.join(audio_dir, f"{filename}_{page}.mp3")]
        elif os.path.exists(os.path.join(audio_dir, f"{filename}_{page}_part1.mp3")):
            print("Skipping audio transcription, already exists ...")
            page_audio_map[page] = [os.path.join(audio_dir, f"{filename}_{page}_part1.mp3"), \
                                    os.path.join(audio_dir, f"{filename}_{page}_part2.mp3")]
        else:
            page_audio_map[page] = text_to_audio(audio_dir, filename, page, content, voice)
            with open(os.path.join(audio_dir, f"{filename}_{page}.mp3"), 'w') as f:
                f.write(page_audio_map[page])

    return page_audio_map

def text_to_audio(audio_dir: str, filename: str, page: int, content: str, voice: str) -> list:
    client = OpenAI()
    max_characters = 4096

    # Tokenize the content into sentences
    sentences = sent_tokenize(content)

    # Check if the content is under the max token limit
    if len(content) <= max_characters:
        # If it's under the limit, proceed with the original function
        speech_file_path = os.path.join(audio_dir, f"{filename}_{page}.mp3")
        response = client.audio.speech.create(
            model="tts-1",
            voice=voice,
            input=content
        )
        response.stream_to_file(speech_file_path)
        return [speech_file_path]
    else:
        # If it's over the limit, split the content into two parts at a sentence boundary
        mid_index = len(sentences) // 2
        part1 = ' '.join(sentences[:mid_index])
        part2 = ' '.join(sentences[mid_index:])

        # Create audio files for each part
        speech_file_path1 = os.path.join(audio_dir, f"{filename}_{page}_part1.mp3")
        speech_file_path2 = os.path.join(audio_dir, f"{filename}_{page}_part2.mp3")

        response1 = client.audio.speech.create(
            model="tts-1",
            voice=voice,
            input=part1
        )
        response1.stream_to_file(speech_file_path1)

        response2 = client.audio.speech.create(
            model="tts-1",
            voice=voice,
            input=part2
        )
        response2.stream_to_file(speech_file_path2)

        # Return the file paths as a list
        return [speech_file_path1, speech_file_path2]