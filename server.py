from flask import Flask, render_template
from backend import Predictor


predictor = Predictor('backend/models')

app = Flask(__name__)


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
