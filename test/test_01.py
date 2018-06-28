#encoding:utf-8
from flask import Flask, current_app

app = Flask(__name__)

# ctx = app.app_context()
# ctx.push()
# a = current_app
# d = current_app.config['DEBUG']
# print(d)
# ctx.pop()


with app.app_context():
  a = current_app.config['DEBUG']
  print(a)