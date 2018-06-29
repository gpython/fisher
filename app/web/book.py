# encoding:utf-8

from flask import request, render_template, flash

from app.libs.helper import is_isbn_or_key
from app.spider.yushu_book import YuShuBook
from app.forms.book import SearchForm
from app.view_models.book import BookCollection, BookViewModel

from . import web
import json

@web.route('/book/search')
def search():
  """
  保证视图函数中代码是简洁易懂的
  :param q:
  :param page:
  :return:
  """

  form = SearchForm(request.args)
  books = BookCollection()

  if form.validate():
    q = form.q.data.strip()
    page = form.page.data
    isbn_or_key = is_isbn_or_key(q)
    yushu_book = YuShuBook()

    if isbn_or_key == 'isbn':
      yushu_book.search_by_isbn(q)
    else:
      yushu_book.search_by_keyword(q, page)

    books.fill(yushu_book, q)
    print(json.dumps(books, default=lambda o: o.__dict__))

  else:
    flash("Search error")

  return render_template('search_result.html', books=books)


@web.route('/book/<isbn>/detail')
def book_detail(isbn):
  yushu_book = YuShuBook()
  yushu_book.search_by_isbn(isbn)

  book = BookViewModel(yushu_book.first)
  return render_template('book_detail.html', book=book, wishes=[], gifts=[])




