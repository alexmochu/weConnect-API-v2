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

    def __init__(self, username, email, password):
        """
        Initialization of user credentials
        """

        self.username = username
        self.email = email
        self.password = password

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
    biz_description = db.Column(db.String(120))
    owner = db.Column(db.String, db.ForeignKey('users.username'))
    business_categ_id = db.Column(db.Integer, db.ForeignKey('categories.id'))

    def save(self):
        """
        Save a bsuiness to the databse
        """
        db.session.add(self)
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
    business_id = db.Column(db.Integer, db.ForeignKey('businesses.id'))

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
   
