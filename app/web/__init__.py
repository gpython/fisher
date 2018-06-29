#encoding:utf-8

from flask import Blueprint

web = Blueprint('web', __name__)

from . import book
from app.web import auth
from app.web import drift
from app.web import gift
from app.web import main
from app.web import wish