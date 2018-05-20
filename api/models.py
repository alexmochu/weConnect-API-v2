# api/models.py
import jwt
from datetime import datetime, timedelta

from flask import current_app
from flask_bcrypt import Bcrypt

from api import db

class User(db.Model):
    """
    Create User table
    """

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(60), index=True, unique=True)
    username = db.Column(db.String(60), index=True, unique=True)
    password = db.Column(db.String(80)) 

    def __init__(self, username, email, password, public_id):
        """
        Initialization of user credentials
        """
        self.public_id = public_id
        self.username = username
        self.email = email
        self.password = Bcrypt().generate_password_hash(password).decode()

    
    def password_is_valid(self, password):
        """
        Checks the password against it's hash to validates the user's password
        """

        return Bcrypt().check_password_hash(self.password, password)

    def save(self):
        """
        Save a user to the databse
        """

        db.session.add(self)
        db.session.commit()

    
    def generate_token(self, user_id):
        """ Generates the access token"""

        try:
            # set up a payload with an expiration time
            payload = {
                'exp': datetime.utcnow() + timedelta(minutes=60),
                'iat': datetime.utcnow(),
                'sub': user_id
            }
            # create the byte string token using the payload and the SECRET key
            jwt_string = jwt.encode(
                payload,
                current_app.config.get('SECRET_KEY'),
                algorithm='HS512'
            )
            return jwt_string

        except Exception as e:
            # return an error in string format if an exception occurs
            return str(e)

    @staticmethod
    def decode_token(token):
        """Decodes the access token from the Authorization header."""
        try:
            # try to decode the token using our SECRET variable
            payload = jwt.decode(token, current_app.config.get('SECRET_KEY'))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            # the token is expired, return an error string
            response = {"Expired token. Please login to get a new token"}
            return response
        except jwt.InvalidTokenError:
            # the token is invalid, return an error string
            response = {"Invalid token. Please register or login"}
            return response

class Category(db.Model):
    """
    Create Category table
    """

    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50))
    created_by = db.Column(db.String, db.ForeignKey('users.username'))

    def save(self):
        """
        Save a user to the databse
        """
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        """
        Deletes a given category
        """
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        """
        Return a representation of a category instance
        """
        return "<Category: {}>".format(self.category)

class Business(db.Model):
    """
    Create Business Item
    """

    __tablename__ = 'businesses'

    id = db.Column(db.Integer, primary_key=True)
    business = db.Column(db.String(50))
    business_location = db.Column(db.String(50))
    owner = db.Column(db.String, db.ForeignKey('users.username'))
    business_category_id = db.Column(db.Integer, db.ForeignKey('categories.id', ondelete='CASCADE', onupdate='CASCADE'))

    def save(self):
        """
        Save a bsuiness to the databse
        """
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """
        Deletes a given category
        """
        db.session.delete(self)
        db.session.commit()


    def __repr__(self):
        """
        Return a representation of a business instance
        """
        return "<Business: {}>".format(self.business)

class Review(db.Model):
    """
    Create review item
    """

    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    review = db.Column(db.String(600))
    reviewer = db.Column(db.String(50), db.ForeignKey('users.username'))
    business_id = db.Column(db.Integer, db.ForeignKey('businesses.id', ondelete='CASCADE', onupdate='CASCADE'))

    def save(self):
        """
        Save a review to the databse
        """
        db.session.add(self)
        db.session.commit()


    def __repr__(self):
        """
        Return a representation of a review instance
        """
        return "<Review: {}>".format(self.review)
   
class BlacklistToken(db.Model):
    """
    Token Model for storing blacklisted JWT tokens
    """
    __tablename__ = 'blacklist_tokens'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(500), unique=True, nullable=False)

    def __init__(self, token):
        self.token = token

    def save(self):
        """Save token"""
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return '<id: token: {}'.format(self.token)
