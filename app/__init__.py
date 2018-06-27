#encoding:utf-8
from flask import  Flask

def create_app():
  app = Flask(__name__)
  app.config.from_object('config')

  register_blueprint(app)

  return app


def register_blueprint(app):
  from app.web import web

  app.register_blueprint(web)