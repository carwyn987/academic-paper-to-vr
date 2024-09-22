from pathlib import Path
from openai import OpenAI
from tqdm import tqdm
import os


def generate_audio(bin_dir: str, filename: str, cleaned_page_content_map: dict[int,str], voice: str) -> dict[int,str]:

    page_audio_map = dict()

    for page, content in tqdm(cleaned_page_content_map.items(), desc=f"Generating audio for {filename}"):
        page_audio_map[page] = text_to_audio(bin_dir, filename, page, content, voice)

    return page_audio_map

def text_to_audio(bin_dir: str, filename: str, page: int, content: str, voice: str) -> str:

    client = OpenAI()

    # speech_file_path = Path(__file__).parent / "speech.mp3"
    speech_file_path = os.path.join(bin_dir, f"{filename}_{page}.mp3")

    response = client.audio.speech.create(
    model="tts-1",
    voice=voice,
    input=content
    )

    response.stream_to_file(speech_file_path)
    return speech_file_path