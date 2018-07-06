#encoding:utf-8
# from collections import namedtuple

from flask import current_app
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, desc, func
from sqlalchemy.orm import  relationship
from app.models.base import Base, db

from app.spider.yushu_book import YuShuBook

# EachGiftWishCount= namedtuple('EachGiftWishCount', ['count', 'isbn'])

class Gift(Base):
  id = Column(Integer, primary_key=True)
  user = relationship('User')
  uid = Column(Integer, ForeignKey('user.id'))
  isbn = Column(String(15), nullable=False)

  #礼物是否已经送出 默认没有送出
  launched = Column(Boolean, default=False)


  #最近上传图书详细信息
  @property
  def book(self):
    yushu_book = YuShuBook()
    yushu_book.search_by_isbn(self.isbn)
    return yushu_book.first

  #最近的礼物
  #只显示一定数量
  #按照时间倒序排列 最新的排在最前边
  #去重 同一本书籍的礼物不重复出现
  #调用知道遇到all() 或 first() 才会去数据库中查询

  #对象代表一个礼物 具体
  #类代表礼物这个事物 是抽象 不是具体的某一个
  #以下方法 最好使用@classmethod
  @classmethod
  def recent(cls):
    #链式调用
    recent_gift = Gift.query.filter_by(
      launched=False).group_by(
      Gift.isbn).order_by(
      desc(Gift.create_time)).limit(
      current_app.config['RECENT_BOOK_COUNT']).distinct().all()
    # recent_gift = Gift.query.filter_by(launched=False).group_by(Gift.isbn).order_by(Gift.create_time)
    return recent_gift

  #根据用户uid 查询用户的 所有 礼物清单(赠送清单)
  @classmethod
  def get_user_gifts(cls, uid):
    gifts = Gift.query.filter_by(
      uid=uid, launched=False).order_by(
      desc(Gift.create_time)).all()
    return gifts

  #根据传入的一组isbn 到Gift表中检索相应的礼物 并且计算出某个礼物的 Wish心愿数量(想要获取此isbn的人数)
  @classmethod
  def get_wish_counts(cls, isbn_list):
    from app.models.wish import Wish
    count_list = db.session.query(func.count(Wish.id), Wish.isbn).filter(
      Wish.launched==False, Wish.isbn.in_(isbn_list), Wish.status == 1).group_by(
      Wish.isbn).all()
    print(count_list)
    #count_list = [EachGiftWishCount(w[0], w[1]) for w in count_list]
    count_list = [{'count':w[0], 'isbn':w[1]} for w in count_list]
    return count_list
