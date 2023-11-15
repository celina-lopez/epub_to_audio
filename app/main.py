import boto3
import os
from dotenv import load_dotenv
import uuid
import os
from app.audio import generate_audible

load_dotenv(dotenv_path='.env')
session = boto3.Session(
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY"),
    aws_secret_access_key=os.getenv("AWS_SECRET_KEY")
)
s3 = session.resource('s3')
BUCKET = os.getenv("AUDIO_BUCKET")


def epub_to_speech(file):
    file_name = generate_audible(file)
    return upload(file_name)


def upload(file_path):
    uid = str(uuid.uuid4())
    key = f'{uid}.mp3'
    print(f"Uploading {file_path} to {key}")
    s3.meta.client.upload_file(file_path, BUCKET, key)
    return key


def get_url(key):
    return f"https://{BUCKET}.s3.amazonaws.com/{key}"


def allowed_file(file_name):
    return '.' in file_name and \
           file_name.rsplit('.', 1)[1].lower() in ['epub']
