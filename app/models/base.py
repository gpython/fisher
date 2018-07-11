#encoding:utf-8
from datetime import  datetime

from sqlalchemy import Column, SmallInteger, Integer
from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy
from flask_sqlalchemy import BaseQuery
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

#filter_by()->orm.Query->BaseQuery->SQLAlchemy
class Query(BaseQuery):
  #重写基类的filter_by 方法
  #字典的.keys() 列出所有字典的 键
  #super执行基类的函数 并返回
  #先写自己的逻辑 然后调用基类被覆盖的方法 返回
  def filter_by(self, **kwargs):
    if 'status' not in kwargs.keys():
      kwargs['status'] = 1
    return super(Query, self).filter_by(**kwargs)

db = SQLAlchemy(query_class=Query)

# 只作为基类使用 不创建此表
class Base(db.Model):
  # 以下为 不创建表 的 标识
  __abstract__ = True

  #类变量发生在整个类创建的时候
  #status 物品状态 1正常 0软删除
  create_time = Column('create_time', Integer)
  status = Column(SmallInteger, default=1)

  def __init__(self):
    self.create_time = int(datetime.now().timestamp())

  #将数字转换为 datetime可使用的时间戳类型
  @property
  def create_datetime(self):
    if self.create_time:
      return datetime.fromtimestamp(self.create_time)
    else:
      return None

  def set_attrs(self, attrs_dict):
    for key, value in attrs_dict.items():
      print(key, value)
      if hasattr(self, key) and key != 'id':
        setattr(self, key, value)

  def delete(self):
    self.status = 0