#encoding:utf-8

"""
flask 的核心对象app将作为一个属性存在于AppContext的应用上下文中
flask的核心对象在 全局里只有一个 app=create_app()



API数据 --> ViewModel --> 页面
ViewModel 裁剪/修饰/合并

面向对象
描述特征 类变量 实例变量
行为    方法



















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
