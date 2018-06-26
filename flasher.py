#encoding:utf-8
from flask import Flask, jsonify
from helper import is_isbn_or_key
from yushu_book import YuShuBook

app = Flask(__name__)
#载入配置文件
app.config.from_object('config')

@app.route('/book/search/<q>/<page>')
def search(q, page):
  """
  保证视图函数中代码是简洁易懂的
  :param q:
  :param page:
  :return:
  """
  isbn_or_key = is_isbn_or_key(q)
  if isbn_or_key == 'isbn':
    result = YuShuBook.search_by_isbn(q)
  else:
    result = YuShuBook.search_by_keyword(q)
  return jsonify(result)
  #return json.dumps(result), 200, {'content-type':'application/json'}



if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=app.config['DEBUG'], port=81)