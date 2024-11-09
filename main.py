from flask import Flask
from create import main as create
from decode import main as decode

app = Flask(__name__)

@app.route('/')
def _home():
    return create()

@app.route('/create')
def _create():
    return create()

@app.route('/<encoded>')
def _decode(encoded):
    return decode(encoded)

if __name__ == '__main__':
    app.run()