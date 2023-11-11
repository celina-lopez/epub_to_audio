import openai
import os
from dotenv import load_dotenv
import os
from pydub import AudioSegment
from utils import create_temp_file, cleanup
from app.book import convert_epub_to_text, slice_text

load_dotenv(dotenv_path='.env')
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL = 'tts-1'


def speak(content, voice='alloy'):
    temp_file = create_temp_file('mp3')
    response = client.audio.speech.create(
        model=MODEL,
        voice=voice,
        input=content
    )
    response.stream_to_file(temp_file)
    return temp_file


def generate_audible(file):
    text = convert_epub_to_text(file)
    sliced_text = slice_text(text)
    file_paths = []
    for i, text in enumerate(sliced_text):
        file_path = f'{i}.mp3'
        speak(text, file_path)
        file_paths.append(file_path)
    return combine_segments(file_paths)


def combine_segments(file_paths):
    combined = AudioSegment.empty()
    for file_path in file_paths:
        sound = AudioSegment.from_mp3(file_path)
        combined += sound
        cleanup(file_path)
    output_path = create_temp_file('mp3')
    combined.export(output_path, format="mp3")
    return output_path
