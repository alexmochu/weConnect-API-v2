# api/__init__.py

# third-party imports
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

# local imports
from config import app_config

# db variable initialization
db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

        # temporary route
    @app.route('/')
    def hello_world():
        response = jsonify({"message": "Welcome to weConnect_V2"})
        return response

    return app