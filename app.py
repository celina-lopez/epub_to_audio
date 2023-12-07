from flask import Flask, request, render_template, redirect
from app.main import allowed_file, epub_to_speech, get_url
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path='.env')
appz = Flask(__name__)


@appz.route('/', methods=['POST', 'GET'])
def index_create():
    if request.method == 'POST':
        # if request.headers['x-api-key'] != os.getenv("API_KEY") or 'file' not in request.files:
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file and allowed_file(file.filename):
            id = epub_to_speech(file, is_rich=True)
            return redirect(get_url(id))
    elif request.method == 'GET':
        return render_template('index.html')


if __name__ == '__main__':
    appz.run(host='0.0.0.0', port=8000, debug=True)
