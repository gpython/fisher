#encoding:utf-8
from sqlalchemy import Integer, Column, String, ForeignKey, SmallInteger
from sqlalchemy.orm import relationship

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

  #赠送者 Info
  gifter_id = Column(Integer)
  gift_id = Column(Integer)
  gifter_nickname = Column(String(20))

  #赠送状态
  pending = Column('pending', SmallInteger, default=1)

  # requester_id = Column(Integer, ForeignKey('user.id'))
  # requester = relationship('User')
  # gift_id = Column(Integer, ForeignKey('gift_id'))
  # gift = relationship('Gift')
