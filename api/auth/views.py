# api/auth/views.py
import uuid
import datetime
import jwt

# universal imports
from flask import Flask, jsonify, request, make_response, current_app
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash

# local imports
from . import auth
from .. import db
from ..models import User

# authorize and authenticate with jwt token
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'header-access-token' in request.headers:
            token = request.headers['header-access-token']

        if not token:
            return jsonify({'message': 'Token is missing!'})

        try:
            data = jwt.decode(token, current_app.config.get('SECRET_KEY'))
            current_user = User.query.filter_by(username=data['username']).first()

        except: 
            return jsonify({'message': 'Token is inavlid!'})

        return f(current_user, *args, **kwargs)

    return decorated

# create user account
@auth.route('/api/v2/auth/register', methods=['POST'])
def signup():

    data = request.get_json()

    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_user = User(username=data['username'], email=data['email'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'Successfully created an account. Login to access account '})

# login into a registered account
@auth.route('/api/v2/auth/login')
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

    user = User.query.filter_by(username=auth.username).first()

    if not user:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

    if check_password_hash(user.password, auth.password):
        token = jwt.encode({'username': user.username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, current_app.config.get('SECRET_KEY'))

        return jsonify({
                        'message': 'You logged in successfully.',
                        'token' : token.decode('UTF-8')
                        })
    
    return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})
