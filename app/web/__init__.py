#encoding:utf-8

from flask import Blueprint

web = Blueprint('web', __name__)

from . import book

@web.app_errorhandler(404)
def not_found(e):
  return 'Not Found', 404

from app.web import auth
from app.web import drift
from app.web import gift
from app.web import main
from app.web import wish