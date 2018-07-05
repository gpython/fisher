# encoding:utf-8

from flask import request, render_template, flash
from flask_login import current_user

from app.libs.helper import is_isbn_or_key
from app.models.gift import Gift
from app.models.wish import Wish
from app.spider.yushu_book import YuShuBook
from app.forms.book import SearchForm
from app.view_models.book import BookCollection, BookViewModel
from app.view_models.trade import TradeInfo

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
  #初始变量 图书不在 赠送礼物清单 也不在 索要心愿清单中 不可能即在礼物清单也在心愿清单
  #查询 此图书在礼物清单中的用户 此图书在心愿清单中的用户
  #当前用户 指定的isbn图书 即不在赠送礼物清单 也不在索要礼物心愿清单
  has_in_gifts = False
  has_in_wishes = False

  # 查询指定isbn的图书
  # 裁剪指定isbn返回的原始数据 为 想要的数据
  yushu_book = YuShuBook()
  yushu_book.search_by_isbn(isbn)
  book = BookViewModel(yushu_book.first)

  # 当前用户有 指定isbn图书在 赠送礼物清单中
  # 当前用户有 指定isbn图书在 索要礼物心愿清单中
  if current_user.is_authenticated:
    if Gift.query.filter_by(uid=current_user.id, isbn=isbn, launched=False).first():
      has_in_gifts = True

    if Wish.query.filter_by(uid=current_user.id, isbn=isbn, launched=False).first():
      has_in_wishes = True

  # 指定isbn 所有赠送者(礼物清单)的 用户清单
  # 指定isbn 所有索要者(心愿清单)的 用户清单
  trade_gifts = Gift.query.filter_by(isbn=isbn, launched=False).all()
  trade_wishes = Wish.query.filter_by(isbn=isbn, launched=False).all()

  trade_wishes_model = TradeInfo(trade_wishes)
  trade_gifts_model = TradeInfo(trade_gifts)


  return render_template('book_detail.html',
                         book=book, wishes=trade_wishes_model,
                         gifts=trade_gifts_model,
                         has_in_wishes=has_in_wishes,
                         has_in_gifts=has_in_gifts)




