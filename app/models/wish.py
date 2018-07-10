#encoding:utf-8
from app.models.base import Base, db
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, desc, func
from sqlalchemy.orm import relationship

from app.spider.yushu_book import YuShuBook

#心愿模型 (想要书籍信息 想要此书籍用户信息 )
class Wish(Base):
  id = Column(Integer, primary_key=True)
  user = relationship('User')
  uid = Column(Integer, ForeignKey('user.id'))
  isbn = Column(String(15), nullable=False)

  #心愿是否已达成 默认没有
  launched = Column(Boolean, default=False)


  @property
  def book(self):
    yushu_book = YuShuBook()
    yushu_book.search_by_isbn(self.isbn)
    return yushu_book.first


  #获取用户的心愿清单 想要得到书籍的列表
  @classmethod
  def get_user_wishes(cls, uid):
    wishes = Wish.query.filter_by(
      uid=uid, launched=False).order_by(
      desc(Wish.create_time)).all()

    return wishes

  #根据传入的一组isbn 到 赠送清单Gift表中 查询 不同书籍有多少人要赠送此书
  @classmethod
  def get_gifts_counts(cls, isbn_list):
    from app.models.gift import Gift
    count_list = db.session.query(
      func.count(Gift.id), Gift.isbn).filter(
      Gift.launched==False, Gift.isbn.in_(isbn_list), Gift.status==1).group_by(
      Gift.isbn).all()
    count_list = [{'count':w[0], 'isbn':w[1]} for w in count_list]
    return count_list
