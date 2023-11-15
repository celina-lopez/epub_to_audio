from flask import Flask, request, render_template, redirect
from app.main import allowed_file, epub_to_speech, get_url
appz = Flask(__name__)


@appz.route('/', methods=['POST', 'GET'])
def index_create():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file and allowed_file(file.filename):
            id = epub_to_speech(file)
            return redirect(get_url(id))
    elif request.method == 'GET':
        return render_template('index.html')


if __name__ == '__main__':
    appz.run(host='0.0.0.0', debug=True)
