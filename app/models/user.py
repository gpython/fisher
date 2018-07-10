#encoding:utf-8
from math import floor

from flask import current_app
from sqlalchemy import Column, Integer, String, Boolean, Float
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import UserMixin

from app import login_manager
from app.libs.enums import PendingStatus
from app.libs.helper import is_isbn_or_key
from app.models.base import Base, db
from app.models.drift import Drift
from app.models.gift import Gift
from app.models.wish import Wish
from app.spider.yushu_book import YuShuBook


class User(UserMixin, Base):
  __tablename__ = 'user'
  id = Column(Integer, primary_key=True)
  nickname = Column(String(24), nullable=False)
  phone_number = Column(String(18), unique=True)
  _password = Column('password', String(128), nullable=False)      #Column名称为password
  email = Column(String(50), unique=True, nullable=False)
  confirmed = Column(Boolean, default=False)
  beans = Column(Float, default=0)
  send_counter = Column(Integer, default=0)
  receive_counter = Column(Integer, default=0)
  wx_open_id = Column(String(50))
  wx_name = Column(String(32))

  @property
  def password(self):
      return self._password

  @password.setter
  def password(self, raw):
    self._password = generate_password_hash(raw)

  def can_send_drift(self):
    if self.beans < 1:
      return  False
    #每索取到两本书 必须赠送出一本书
    #gift赠送 此id用户 已经送出图书数量
    success_gifts_count = Gift.query.filter_by(
      uid=self.id, launched=True).count()
    #已索取到的书籍数量
    success_receive_count = Drift.query.filter_by(
      requester_id=self.id, pending=PendingStatus.Success).count()

    #每索取到两本书 必须赠送出一本书
    return True if floor(success_receive_count/2) <= floor(success_gifts_count) else False

  def check_password(self, raw):
    return check_password_hash(self._password, raw)

  #判断isbn是否存在 或者isbn是否在正确的isbn编号
  #可以保存到赠送清单
  def can_save_to_list(self, isbn):
    if is_isbn_or_key(isbn) != 'isbn':
      return False
    yushu_book = YuShuBook()
    yushu_book.search_by_isbn(isbn)

    if not yushu_book.first:
      return False

    #不允许一个用户同时赠送多本相同的图书
    #一个用户不可能同时成为赠送者或者索要者

    #当前isbn图书编号 已经存在于用户的赠送清单中 并且还没有赠送出去 （不允许同时赠送多本图书 [未赠送出去]）
    gifting = Gift.query.filter_by(uid=self.id, isbn=isbn, launched=False).first()
    #当前isbn图书编号 是否存在于用户的心愿清单里
    wishing = Wish.query.filter_by(uid=self.id, isbn=isbn, launched=False).first()

    #即不在赠送清单 也不在心愿清单中  才能添加
    if not gifting and not wishing:
      return True
    else:
      return False


  def generate_token(self, expiration=600):
    s = Serializer(current_app.config['SECRET_KEY'], expiration)
    return s.dumps({'id': self.id}).decode('utf-8')

  @staticmethod
  def reset_password(token, new_password):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
      data = s.loads(token.encode('utf-8'))
    except Exception as e:
      print(e)
      return False

    uid = data.get('id')
    with db.auto_commit():
      user = User.query.get(uid)
      user.password = new_password
    return True

  @property
  def summary(self):
      return dict(
        nickname = self.nickname,
        beans = self.beans,
        email = self.email,
        send_receive = str(self.send_counter) + '/' + str(self.receive_counter)
      )


@login_manager.user_loader
def get_user(uid):
  return User.query.get(int(uid))