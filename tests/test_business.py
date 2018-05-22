import unittest
import os
import json
from flask_testing import TestCase

from api import create_app, db

class AuthTestCase(unittest.TestCase):
     """Test case for the auth blueprint."""
     def setUp(self):
        """Set up test variables."""
        self.app = create_app(config_name="testing")
        self.app.config.update(SQLALCHEMY_DATABASE_URI='postgresql+psycopg2://postgres:@localhost:5432/postgres')
        self.app_context = self.app.app_context()
        self.app_context.push()
        # initialize the test client
        self.client = self.app.test_client
        # This is the user test json data with a predefined email and password

        with self.app.app_context():
            # create all tables
            db.session.close()
            db.drop_all()
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

     def get_new_token(self):
        """register and login a user to get an access token"""
        self.register_user(self.user_data2)
        result = self.login_user(self.login_data2)
        header_access_token = json.loads(result.data.decode())['header_access_token']
        return header_access_token


     def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()

if __name__ == "__main__":
    unittest.main()
