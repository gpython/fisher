#encoding:utf-8

from flask import Blueprint

web = Blueprint('web', __name__)

from . import book
from . import index