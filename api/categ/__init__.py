# api/categ/__init__.py

from flask import Blueprint

categ = Blueprint('categ', __name__)

from . import views