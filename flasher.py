#encoding:utf-8
from flask import Flask

app = Flask(__name__)

@app.route('/index')
def index():
  return "Hello Index"

app.run(host='0.0.0.0', debug=True, port=81)