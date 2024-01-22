import flask
import sqlite3

app = flask.Flask(__name__, template_folder='views')

@app.route('/', methods=['GET'])
def home():
   