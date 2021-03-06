# api/auth/views.py
import uuid
import datetime
import jwt
import re

# universal imports
from flask import Flask, jsonify, request, make_response, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash

# local imports
from . import auth
from .. import db
from ..models import User, BlacklistToken

# authorize and authenticate with jwt token
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        access_token = request.headers['header-access-token']
        blacklisted = BlacklistToken.query.filter_by(token=access_token).first()

        if blacklisted:
            response = {"message": "Logged out. Please login again!" }
            return make_response(jsonify(response)), 401

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

    if not re.match("^[a-zA-Z0-9_]*$", data['user']['username']):
        # Check username special characters        
        response = {'error':'Username cannot have special characters!'}
        return make_response(jsonify(response)), 302
    if len(data['user']['username'].strip())<5:
        # Checkusername length
        # return an error message if requirement not met
        # return a 403 - auth failed
        response = {'error':'Username must be more than 5 characters'}
        return make_response(jsonify(response)), 302
    if not re.match(r"(^[a-zA-Z0-9_.]+@[a-zA-Z0-9-]+\.[a-z]+$)", data['user']['email']):
        # Check email validity
        response = {'error':'Provide a valid email!'}
        return make_response(jsonify(response)), 302
    if (data['user']['password']!=data['user']['confirm_password']):
        # Verify passwords are matching
        response = {'error':'The passwords should match!'}
        return make_response(jsonify(response)), 302
    if len(data['user']['password']) < 5 or not re.search("[a-z]", data['user']['password']) or not\
    re.search("[0-9]", data['user']['password']) or not re.search("[A-Z]", data['user']['password']) \
    or not re.search("[$#@*!%^]", data['user']['password']):
        # Check password strength
        response = {'error':'Password length should be more than 5 characters, have one lowercase, uppercase, number and special character'}
        return make_response(jsonify(response)), 302

    existing_email = User.query.filter_by(email=data['user']['email']).first()
    if existing_email:
        response = {"error" : "An account with that email already exists!"}
        return make_response(jsonify(response)), 302
    existing_username = User.query.filter_by(username=data['user']['username']).first()
    if existing_username:
        response = {"error" : "An account with that username already exists!"}
        return make_response(jsonify(response)), 302

    username = data['user']['username']
    email = data['user']['email']
    password = data['user']['password']
    confirm_password = data['user']['confirm_password']

    try:
        #hashed_password = generate_password_hash(data['password'], method='sha256')
        new_user = User(public_id=str(uuid.uuid4()), username=data['user']['username'], email=data['user']['email'], password=data['user']['password'])
        db.session.add(new_user)
        db.session.commit()

        response = {
            "user":{'message': 'Successfully created an account. Login to access account'}
        }
        # return a response notifying the user that they registered successfully            
    except Exception as e:
        # An error occured, therefore return a string message containing the error
        response = {'message': str(e)}
        return make_response(jsonify(response)), 401
    return make_response(jsonify(response)), 201

# login into a registered account
@auth.route('/api/v2/auth/login', methods=['POST'] )
def login():
    """Handle POST request for this view. Url ---> /auth/login"""
    try:
        # Get the user object using their email (unique to every user)
        req = request.get_json()
        user = User.query.filter_by(username=req['credentials']['username']).first()
        # Try to authenticate the found user using their password
        
        if user and user.password_is_valid(req['credentials']['password']):
            print(str(user.username))
            
            # Generate the access token. This will be used as the authorization header
            header_access_token = jwt.encode({'username': user.username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, current_app.config.get('SECRET_KEY'))
            print(header_access_token)
            if header_access_token:
                response = {
                  "user" :  {
                    'message': 'You logged in successfully.',
                    'header_access_token': header_access_token.decode()
                }
                }
                return make_response(jsonify(response)), 200
        else:
            # User does not exist. Therefore, we return an error message
            response = {'error': 'Invalid username or password, Please try again'}
            return make_response(jsonify(response)), 401

    except Exception as e:
        # Create a response containing an string error message
        response = {'error': str(e)}
        # Return a server error using the HTTP Error Code 500 (Internal Server Error)
        return make_response(jsonify(response)), 500
       
@auth.route('/api/v2/auth/reset-password', methods=['PUT'])
@token_required
def reset_password(current_user, data):
    """Handle PUT request for this view. Url ---> /api/v2/auth/reset-password"""                    
    user = User.query.filter_by(username=data['username']).first()
    req = request.get_json()
    new_password = req['new_password']
    confirm_password = req['confirm_password']
    print(new_password)
    # Try to authenticate user id and password fields
    if new_password!=confirm_password:
        # Passwords aren't matching. Therefore, we return an error message
        response = {'message': 'Enter matching passwords'}
        return make_response(jsonify(response)), 400
    try:
        # Edit the password
        user.password = Bcrypt().generate_password_hash(new_password).decode()
        user.save()
        response = {'message': 'Password changed successfully.'}
    except Exception as e:
        # Create a response containing an string error message
        response = {'message': str(e)}
        # Return a server error using the HTTP Error Code 500 (Internal Server Error)
        return make_response(jsonify(response)), 500
    return make_response(jsonify(response)), 200

@auth.route('/api/v2/auth/logout', methods=['POST'])
@token_required
def logout(current_user, user_id):
    header_access_token = request.headers['header-access-token']
    if user_id['username'] != User.decode_token(header_access_token):
        print(user_id)
        print(User.decode_token(header_access_token))
        response = {'message': 'An error occured.'}
        return make_response(jsonify(response)), 403            
    try:
        # insert the token
        blacklist_token = BlacklistToken(token=header_access_token)
        blacklist_token.save()
        response = {
            'message': 'Successfully logged out.'
        }
        return make_response(jsonify(response)), 200
    except Exception as e:
        response = {
            'message': e
        }
        return make_response(jsonify(response)), 200 
