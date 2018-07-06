#encoding:utf-8
from flask import  Flask
from app.models.base import db
from flask_login import LoginManager
from flask_mail import Mail

login_manager = LoginManager()
mail = Mail()

def create_app():
  app = Flask(__name__)
  app.config.from_object('app.setting')
  app.config.from_object('app.secure')

  register_blueprint(app)
  db.init_app(app)

  login_manager.init_app(app)
  login_manager.login_view = 'web.login'
  login_manager.login_message = 'Please Login or Register'

  mail.init_app(app)

  with app.app_context():
    db.create_all()

  return app


def register_blueprint(app):
  from app.web import web

  app.register_blueprint(web)