from flask import Flask, render_template, flash, request, redirect
from backend import Predictor
from werkzeug.utils import secure_filename
import os


predictor = Predictor('backend/models')

UPLOAD_FOLDER = './temp'
ALLOWED_EXTENSIONS = {'nii.gz'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def server():
    return index()


@app.route('/brainchop')
def index():
    models = []
    for index, model in enumerate(predictor.models):
        item = model['meta']
        item['id'] = index
        item['value'] = item['name']
        models.append(item)
    print('available models:')
    for model in models:
        print(model['name'])
    return render_template('index.html', available_models=models)


def allowed_file(filename):
    return True
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def process_file():
    if request.method == 'POST':
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        print(f'Received file {file.filename} for processing')
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            if not os.path.exists(app.config['UPLOAD_FOLDER']):
                os.makedirs(app.config['UPLOAD_FOLDER'])
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return filename
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''
