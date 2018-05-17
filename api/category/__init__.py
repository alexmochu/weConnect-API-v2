# api/categ/__init__.py

from flask import Blueprint

category = Blueprint('category', __name__)

from . import views