#encoding:utf-8

from flask import jsonify, request
from flask import Blueprint

from helper import is_isbn_or_key
from yushu_book import YuShuBook

from . import web


@web.route('/book/search')
def search():
  """
  保证视图函数中代码是简洁易懂的
  :param q:
  :param page:
  :return:
  """
  q = request.args.get('q', 'python')
  page = request.args.get('page', 1)
  a = request.args.to_dict()
  print(a)

  isbn_or_key = is_isbn_or_key(q)

  if isbn_or_key == 'isbn':
    result = YuShuBook.search_by_isbn(q)
  else:
    result = YuShuBook.search_by_keyword(q)
  return jsonify(result)