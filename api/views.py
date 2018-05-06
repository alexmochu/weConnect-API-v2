# api/views.py
import uuid
import datetime
import jwt

# universal imports
from flask import Flask, jsonify, request, make_response
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash

from api.models import User

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
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.query.filter_by(username=data['username']).first()

        except: 
            return jsonify({'message': 'Token is inavlid!'})

        return f(current_user, *args, **kwargs)

    return decorated

# home route
@app.route('/')
def hello_world():
    response = jsonify({"message": "Welcome to weConnect_V2"})
    return response

# create user account
@app.route('/api/v2/auth/register', methods=['POST'])
def signup():

    data = request.get_json()

    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_user = User(username=data['username'], email=data['email'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'Successfully created an account. Login to access account '})

@app.route('/api/v2/auth/login')
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

    user = User.query.filter_by(username=auth.username).first()

    if not user:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

    if check_password_hash(user.password, auth.password):
        token = jwt.encode({'username': user.username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])

        return jsonify({'token' : token.decode('UTF-8')})
    
    return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

# user temporary dashboard route
@app.route('/token_ok')
@token_required
def token_ok(current_user):
    if not current_user:
        return jsonify({'message': 'Cannot perform that function! Please login'})

    response = jsonify({"message": "Yeaah!! You have successfully authenticated your token"})
    return response