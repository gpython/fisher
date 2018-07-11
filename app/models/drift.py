#encoding:utf-8
from sqlalchemy import Integer, Column, String, ForeignKey, SmallInteger
from sqlalchemy.orm import relationship

from app.libs.enums import PendingStatus
from app.models.base import Base


class Drift(Base):
  #每次交易信息
  id = Column(Integer, primary_key=True)

  #邮寄信息
  recipient_name = Column(String(20), nullable = False)
  address = Column(String(100), nullable=True)
  message = Column(String(200))
  mobile = Column(String(20), nullable=False)

  #书籍 Info
  isbn = Column(String(13))
  book_title = Column(String(50))
  book_author = Column(String(30))
  book_img = Column(String(50))

  #请求者 Info
  requester_id = Column(Integer)
  requester_nickname = Column(String(20))

  #赠送者 Info+
  gifter_id = Column(Integer)
  gift_id = Column(Integer)
  gifter_nickname = Column(String(20))

  #赠送状态
  _pending = Column('pending', SmallInteger, default=1)


  @property
  def pending(self):
    #数字类型转换成枚举类型
    return PendingStatus(self._pending)

  #枚举类型转换成数字类型
  @pending.setter
  def pending(self, status):
    self._pending = status.value

  # requester_id = Column(Integer, ForeignKey('user.id'))
  # requester = relationship('User')
  # gift_id = Column(Integer, ForeignKey('gift_id'))
  # gift = relationship('Gift')
