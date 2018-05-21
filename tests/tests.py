import unittest
import os
import json
from flask_testing import TestCase
from werkzeug.security import generate_password_hash, check_password_hash

from api import create_app, db

class AuthTestCase(unittest.TestCase):
     """Test case for the auth blueprint."""
     def setUp(self):
        """Set up test variables."""
        self.app = create_app(config_name="testing")
        #self.app.config.update(SQLALCHEMY_DATABASE_URI='postgresql://postgres:mypassword@localhost/weConnect_test')
        self.app_context = self.app.app_context()
        self.app_context.push()
        # initialize the test client
        self.client = self.app.test_client
        # This is the user test json data with a predefined email and password
        hashed_password = generate_password_hash('J@yd33n', method='sha256')
        self.user_data = {
            'username':'bigdolf',
            'email': 'test@example.com',
            'password': 'J@yd33n',
            'confirm_password': 'J@yd33n'
        }
        self.login_data = {
            'username': 'bigdolf',
            'password': 'J@yd33n'
        }

        self.user_data2 = {
            'username':'smalldolf',
            'email': 'test1@example.com',
            'password': 'J@yd33n',
            'confirm_password': 'J@yd33n'
        }

        self.login_data2 = {
            'username': 'smalldolf',
            'password': 'J@yd33n'
        }

        with self.app.app_context():
            # create all tables
            db.create_all()

     def register_user(self, data):
        return self.client().post('api/v2/auth/register', data=json.dumps(data), content_type='application/json' )

     def login_user(self, data):
        return self.client().post('/api/v2/auth/login', data=json.dumps(data), content_type='application/json' )

     def test_registration(self):
        """Test user registration works correcty."""
        res = self.register_user(self.user_data)
        # get the results returned in json format
        result = json.loads(res.data.decode())
        # assert that the request contains a success message and a 201 status code
        self.assertEqual(result['message'], "Successfully created an account. Login to access account")
        self.assertEqual(res.status_code, 201)

     def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()

if __name__ == "__main__":
    unittest.main()
