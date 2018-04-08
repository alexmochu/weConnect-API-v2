# api/views.py
import uuid
import datetime
import jwt

# universal imports
from flask import jsonify, request, session
from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy

# local imports

# initialize the api
app = FlaskAPI(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config.from_pyfile('config.py')

db = SQLAlchemy()

db.init_app(app)

# home route
@app.route('/')
def hello_world():
    response = jsonify({"message": "Welcome to weConnect_V2"})
    return response