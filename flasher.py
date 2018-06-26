#encoding:utf-8
from flask import Flask, make_response


app = Flask(__name__)
#载入配置文件
app.config.from_object('config')

@app.route('/book/search/<q>/<page>')
def search(q, page):
  """

  :param q: 普通关键字
  :param page: 页数
  :return:
  """
  #以下代码是用来判断q是isbn还是关键字 逻辑判断写在此非常不好
  isbn_or_key = 'key'
  if len(q) == 13 and q.isdigit():
    isbn_or_key = 'isbn'
  short_q = q.replace('-', '')
  if '-' in q and len(short_q) == 10 and short_q.isdigit:
    isbn_or_key = 'isbn'
  pass


if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=app.config['DEBUG'], port=81)