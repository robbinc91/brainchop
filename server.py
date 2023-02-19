from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def server():
    return 'Hello, World!'


@app.route('/brainchop')
def index():
    return render_template('index.html')
