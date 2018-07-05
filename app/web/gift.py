#encoding:utf-8
from flask import current_app, flash, render_template, url_for, redirect
from flask_login import login_required, current_user

from app.models.base import db
from app.models.gift import Gift
from app.view_models.gift import MyGifts
from . import web
__author__ = '七月'


#当前用户的礼物赠送清单
@web.route('/my/gifts')
@login_required
def my_gifts():
  uid = current_user.id
  #查询出当前用户的所有礼物清单
  gifts_of_mine = Gift.get_user_gifts(uid)
  #根据礼物清单 查询每个礼物的想要的人的数量
  isbn_list = [gift.isbn for gift in gifts_of_mine]
  wish_count_list = Gift.get_wish_counts(isbn_list)

  view_model = MyGifts(gifts_of_mine, wish_count_list)

  return render_template('my_gifts.html', gifts=view_model.gifts)
  


#赠送此书
@web.route('/gifts/book/<isbn>')
@login_required
def save_to_gifts(isbn):
  if current_user.can_save_to_list(isbn):
    with db.auto_commit():
      gift = Gift()
      gift.isbn = isbn
      gift.uid = current_user.id
      current_user.beans += current_app.config['BEANS_UPLOAD_ONE_BOOK']
      db.session.add(gift)

  else:
    flash('此书已存在于你的赠送清单或心愿清单中 不可重复添加')

  return redirect(url_for('web.book_detail', isbn=isbn))

@web.route('/gifts/<gid>/redraw')
def redraw_from_gifts(gid):
  pass



