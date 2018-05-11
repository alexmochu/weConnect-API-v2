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

        return f(current_user, data, *args, **kwargs)

    return decorated

# create user account
@auth.route('/api/v2/auth/register', methods=['POST'])
def signup():

    data = request.get_json()

    #hashed_password = generate_password_hash(data['password'], method='sha256')
    new_user = User(username=data['username'], email=data['email'], password=data['password'])
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'Successfully created an account. Login to access account'}), 201

# login into a registered account
@auth.route('/api/v2/auth/login', methods=['POST'] )
def login():
    """Handle POST request for this view. Url ---> /auth/login"""
    try:
        # Get the user object using their email (unique to every user)
        req = request.get_json()
        user = User.query.filter_by(username=req['username'], password=req['password']).first()
        # Try to authenticate the found user using their password
        if user:
            # Generate the access token. This will be used as the authorization header
            header_access_token = jwt.encode({'username': user.username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, current_app.config.get('SECRET_KEY'))
            if header_access_token:
                response = {
                    'message': 'You logged in successfully.',
                    'header_access_token': header_access_token.decode()
                }
                return make_response(jsonify(response)), 200
        else:
            # User does not exist. Therefore, we return an error message
            response = {'message': 'Invalid username or password, Please try again'}
            return make_response(jsonify(response)), 401

    except Exception as e:
        # Create a response containing an string error message
        response = {'message': str(e)}
        # Return a server error using the HTTP Error Code 500 (Internal Server Error)
        return make_response(jsonify(response)), 500
