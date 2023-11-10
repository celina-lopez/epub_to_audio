import boto3
import os
from dotenv import load_dotenv
import uuid
import os
from app.book import convert_epub_to_text, slice_text
from app.audio import speak, generate_audible

load_dotenv(dotenv_path='.env')
session = boto3.Session(
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY"),
    aws_secret_access_key=os.getenv("AWS_SECRET_KEY")
)
s3 = session.resource('s3')
BUCKET = os.getenv("AUDIO_BUCKET")


def epub_to_speech(file):
    text = convert_epub_to_text(file)
    sliced_text = slice_text(text)
    file_paths = []
    for i, text in enumerate(sliced_text):
        file_path = f'{i}.mp3'
        speak(text, file_path)
        file_paths.append(file_path)
    generate_audible(file_paths, 'output.mp3')
    return file_paths


def upload(file_path):
    uid = str(uuid.uuid4())
    key = f'{uid}.mp3'
    s3.meta.client.upload_file(file_path, BUCKET, key)
    return f"https://{BUCKET}.s3.amazonaws.com/{key}"


def allowed_file(file_name):
    return '.' in file_name and \
           file_name.rsplit('.', 1)[1].lower() in ['epub']
