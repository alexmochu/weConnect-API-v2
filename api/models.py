# api/models.py

from api import db

class User(db.Model):
    """
    Create User table
    """

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), index=True, unique=True)
    username = db.Column(db.String(60), index=True, unique=True)
    password = db.Column(db.String(80)) 

    def __init__(self, username, email):
        """
        Initialization of user credentials
        """

        self.username = username
        self.email = email

class Category(db.Model):
    """
    Create Category table
    """

    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50))
    description = db.Column(db.String(120))
    created_by = db.Column(db.String, db.ForeignKey('users.username'))

    def save(self):
        """
        Save a user to the databse
        """
        db.session.add(self)
        db.session.commit()
