# api/business/__init__.py

from flask import Blueprint

business = Blueprint('business', __name__)

from . import views