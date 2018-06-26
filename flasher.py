#encoding:utf-8
from flask import Flask


app = Flask(__name__)
#载入配置文件
app.config.from_object('config')

@app.route('/index')
def index():
  return "Hello Index"


if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=app.config['DEBUG'], port=81)