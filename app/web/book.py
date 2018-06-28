# encoding:utf-8

from flask import jsonify, request

from app.libs.helper import is_isbn_or_key
from app.spider.yushu_book import YuShuBook
from app.forms.book import SearchForm
from app.view_models.book import BookViewModel

from . import web


@web.route('/book/search')
def search():
  """
  保证视图函数中代码是简洁易懂的
  :param q:
  :param page:
  :return:
  """
  # q = request.args.get('q', 'python')
  # page = request.args.get('page', 1)

  form = SearchForm(request.args)
  if form.validate():
    q = form.q.data.strip()
    page = form.page.data

    isbn_or_key = is_isbn_or_key(q)

    if isbn_or_key == 'isbn':
      result = YuShuBook.search_by_isbn(q)
      result = BookViewModel.package_single(result, q)
    else:
      result = YuShuBook.search_by_keyword(q)
      result = BookViewModel.package_collection(result, q)
    return jsonify(result)
  return jsonify(form.errors)


