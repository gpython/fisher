#encoding:utf-8

"""
flask 的核心对象app将作为一个属性存在于AppContext的应用上下文中
flask的核心对象在 全局里只有一个 app=create_app()



API数据 --> ViewModel --> 页面
ViewModel 裁剪/修饰/合并

面向对象
描述特征 类变量 实例变量
行为    方法


wtfrom 表单
form = RegisterForm(request.form)
form.data  => {'email': 'xxxx@xxxx.com', 'password': 'ssdfsd', 'nickname': 'Goo67le'}
form.email => <input id="email" name="email" required type="text" value="zhuwn@juzhongjoy.com">
form.email.data == form.data['email'] => 'xxxx@xxxx.com'
















"""

import json
class Books:
  gloabl_prams = 'This is global params'
  def __init__(self):
    self.title = 'Python'
    self.isbn = 1111111
    self.relations = [{'title': 'simple', 'isbn': 22222},
                      {'title': 'breatu', 'isbn': 33333}]
book = Books()
print(json.dumps(book, default=lambda o:o.__dict__))


#######################with 的实现
class WithFunc():
  #进入上下文管理器时 执行
  def __enter__(self):
    print("Enter")
    return self

  #退出上下文管理器时 执行
  def __exit__(self, exc_type, exc_value, tb):
    print('EXIT')

  def query(self):
    print('query data')


with WithFunc() as r:
  r.query()

####################contextmanager 可以简化以上with的定义 可以不用定义__enter__ __exit__这两个方法
#实例 1
from contextlib import contextmanager
class WithFunc():
  def query(self):
    print("Query contextmanager")

@contextmanager
def with_contextmanager():
  #使用contextmanager 进入上下文管理器 执行以下语句
  print('contextmanager enter')
  #正式执行 想要执行的函数 挂起 yield函数执行流程的中断
  #yield挂起 等待执行with里的内容
  yield WithFunc()
  #使用contextmanager 进入上下文管理器 当执行完毕时 执行以下语句
  print('contextmanager exit')

with with_contextmanager() as r:
  r.query()

#实例 2
from contextlib import contextmanager
@contextmanager
def book_mark():
  print('<<', end='')
  yield
  print('>>', end='')

with book_mark:
  print('Fluent Python', end='')

#实例 3
from flask_sqlalchemy import  SQLAlchemy as _SQLAlchemy
from contextlib import contextmanager

#数据提交回滚操作
#继承SQLAlchemy 并添加新的方法
class SQLAlchemy(_SQLAlchemy):
  @contextmanager
  def auto_commit(self):
    try:
      #yield挂起 等待执行with语句里的内容
      yield
      self.session.commit()
    except Exception as e:
      db.session.rollback()
      raise e

db = SQLAlchemy()

with db.auto_commit():
  pass

############# 修改filter_by

#filter_by 继承自 sqlalchemy 模块 orm目录下query文件中Query类 即orm.Query
#flask_sqlalchemy 实现了BaseQuery类 继承自orm.Query 并实现了get_or_404 first_or_404 paginate 等函数
#现在可自定义 Query类 继承BaseQuery类 实现想要的其他功能
#字典的.keys() 获得所有字典的键的集合