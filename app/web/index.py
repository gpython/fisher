#encoding:utf-8
from . import  web

@web.route('/index')
def index():
  return 'Hello'