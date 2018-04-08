# api/__init__.py

# local imports
from api.views import app

def create_app():
    """Initialize the app"""
    return app