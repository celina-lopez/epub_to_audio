from flask import Flask, request, render_template, redirect, url_for
from app.main import allowed_file, epub_to_speech

appz = Flask(__name__)


@appz.route('/', methods=['POST', 'GET'])
def index_create():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file and allowed_file(file.filename):
            file_paths = epub_to_speech(file)
            # TODO: upload to s3
            return redirect(url_for('show', id='124'))  # update later
    elif request.method == 'GET':
        return render_template('index.html')


@appz.route('/<id>', methods=['GET'])
def show(id):
    if request.method == 'GET':
        return render_template('show.html', id=id)


if __name__ == '__main__':
    appz.run(host='0.0.0.0', debug=True)
