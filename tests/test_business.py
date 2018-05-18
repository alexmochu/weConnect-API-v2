
import unittest
from flask import jsonify
import json

from flask_testing import TestCase
from api import create_app, db

class BusinessTestCase(unittest.TestCase):
    """
    This class represents the business test case
    """

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        #self.app.config.update(SQLALCHEMY_DATABASE_URI='postgresql://postgres:mypassword@localhost/weConnect_test')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client
        self.business = {"business":"Maendeleo","description":"Progress is the way"}
        self.user_data = {'username': "bigdolf", 'email': "big@dolf.com", 'password': "J@yd33n"}
        self.login_data = {'username': "bigdolf", 'password': "J@yd33n"}
        self.user_data2 = {'username': "smalldolf", 'email': "small@dolf.com",'password': "sTr0ng3st@dolf"}
        self.login_data2 = {'username': "smalldolf", 'password': "sTr0ng3st@dolf"}

        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()

    def register_user(self, data):
        return self.client().post('api/v2/auth/register', data=json.dumps(data), content_type='application/json' )

    def login_user(self, data):
        return self.client().post('/api/v2/auth/login', data=json.dumps(data), content_type='application/json' )

    def get_token(self):
        """register and login a user to get an access token"""
        self.register_user(self.user_data)
        result = self.login_user(self.login_data)
        header_access_token = json.loads(result.data.decode())['header_access_token']
        return header_access_token

    def tearDown(self):
        """teardown all initialized variables."""
        # drop all tables
        db.session.remove()
        db.drop_all()
    

if __name__ == "__main__":
    unittest.main()

