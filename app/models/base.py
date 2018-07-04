#encoding:utf-8
from datetime import  datetime

from sqlalchemy import Column, SmallInteger, Integer
from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy
from contextlib import contextmanager

#重写SQLAlchemy 并添加新方法
class SQLAlchemy(_SQLAlchemy):
  @contextmanager
  def auto_commit(self):
    try:
      yield
      self.session.commit()
    except Exception as e:
      self.session.rollback()
      raise e

db = SQLAlchemy()

# 只作为基类使用 不创建此表
class Base(db.Model):
  # 以下为 不创建表 的 标识
  __abstract__ = True

  #类变量发生在整个类创建的时候
  create_time = Column('create_time', Integer)
  status = Column(SmallInteger, default=1)

  def __init__(self):
    self.create_time = int(datetime.now().timestamp())

  def set_attrs(self, attrs_dict):
    for key, value in attrs_dict.items():
      print(key, value)
      if hasattr(self, key) and key != 'id':
        setattr(self, key, value)
