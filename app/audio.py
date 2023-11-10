import openai
import os
from dotenv import load_dotenv
import os
from pydub import AudioSegment
from utils import create_temp_file, cleanup

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


def generate_audible(file_paths, output_path='output.mp3'):
    combined = AudioSegment.empty()
    for file_path in file_paths:
        sound = AudioSegment.from_mp3(file_path)
        combined += sound
        cleanup(file_path)
    combined.export(output_path, format="mp3")
