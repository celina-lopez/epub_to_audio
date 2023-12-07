import openai
import os
from dotenv import load_dotenv
import os
from pydub import AudioSegment
from app.utils import create_temp_file, cleanup
from app.book import convert_epub_to_text, slice_text, get_quotes

load_dotenv(dotenv_path='.env')
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL = 'tts-1'
GENDERED_VOICES = {
    'M': 'echo',
    'F': 'nova'
}


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
        file_path = speak(text)
        file_paths.append(file_path)
    return combine_segments(file_paths)


def slice_around_word(text, word):
    index = text.find(word)
    if index != -1:
        before = text[:index].strip()
        after = text[index+len(word):].strip()
        return before, after
    else:
        return None, None


def generate_rich_audible(file):
    text = convert_epub_to_text(file)
    sliced_text = slice_text(text)
    file_paths = []
    for i, text in enumerate(sliced_text):
        process_segment(text, file_paths)
    return combine_segments(file_paths)


def process_segment(text, file_paths):
    gendered_quotes = get_quotes(text)
    if gendered_quotes == []:
        speak_and_append_to_filepath(file_paths, text)
        return
    for quote in gendered_quotes:
        before, after = slice_around_word(text, quote[0])
        if before:
            speak_and_append_to_filepath(file_paths, before)
            speak_and_append_to_filepath(
                file_paths, quote[0], GENDERED_VOICES[quote[1]])
    if after:
        speak_and_append_to_filepath(file_paths, after)


def speak_and_append_to_filepath(file_paths, text, voice='alloy'):
    file_path = speak(text, voice=voice)
    file_paths.append(file_path)


def combine_segments(file_paths):
    combined = AudioSegment.empty()
    for file_path in file_paths:
        sound = AudioSegment.from_mp3(file_path)
        combined += sound
        cleanup(file_path)
    output_path = create_temp_file('mp3')
    combined.export(output_path, format="mp3")
    return output_path
