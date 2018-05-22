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
        self.app.config.update(SQLALCHEMY_DATABASE_URI='postgresql+psycopg2://postgres:@localhost:5432/postgres')
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
        self.user_data3 = {
            'username':'chris# evans',
            'email': 'test@example.com',
            'password': 'J@yd33n',
            'confirm_password': 'J@yd33n'
                }

        self.user_data4 = {
            'username':'chris#evans',
            'email': 'test@example.com',
            'password': 'J@yd33n',
            'confirm_password': 'J@yd33n'
                }

        with self.app.app_context():
            # create all tables
            db.session.close()
            db.drop_all()
            db.create_all()

     def register_user(self, data):
        return self.client().post('api/v2/auth/register', data=json.dumps(data), content_type='application/json' )

     def login_user(self, data):
        return self.client().post('/api/v2/auth/login', data=json.dumps(data), content_type='application/json' )

     def test_valid_email(self):
        invalid_mail = {
            'username':'chrisevans',
            'email': 'test@examplecom',
            'password': 'J@yd33n',
            'confirm_password': 'J@yd33n'
                }
        res = self.register_user(invalid_mail)
        print(res)
        # get the results returned in json format
        result = res.data
        # assert that the request contains a success message and a 201 status code
        self.assertIn("Provide a valid email!", str(result))
        self.assertEqual(res.status_code, 302)

     def test_username_characters(self):
        reg_data = {
            'username':'chris#evans',
            'email': 'test@example.com',
            'password': 'J@yd33n',
            'confirm_password': 'J@yd33n'
                }
        res = self.register_user(reg_data)
        print(res)
        # get the results returned in json format
        result = res.data
        # assert that the request contains a success message and a 201 status code
        self.assertIn("Username cannot have special characters!", str(result))
        self.assertEqual(res.status_code, 200)

    
     def test_password_mismatch(self):
        """Test if passwords are matching."""
        reg_data = {
                    'username':'chrisevans',
                    'email': 'test@example.com',
                    'password': 'J@yd33n',
                    'confirm_password': 'J@yd33na'
                }

        res = res = self.register_user(reg_data)
        # get the results returned in json format
        result = res.data
        # assert that the request contains an error message and a 403 status code
        self.assertIn("The passwords should match!", str(result))
        self.assertEqual(res.status_code, 200)

     def test_username_length(self):
        """Test username length."""
        reg_data = {
                    'username':'csi',
                    'email': 'test@example.com',
                    'password': 'J@yd33n',
                    'cpassword': 'J@yd33n'
                }

        res = self.register_user(reg_data)
        # get the results returned in json format
        result = res.data
        # assert that the request contains an error message and a 403 status code
        self.assertIn("Username must be more than 5 characters", str(result))
        self.assertEqual(res.status_code, 200)

     def test_password_strength(self):
        """Test if password is strong."""
        reg_data = {
                    'username':'chrisevans',
                    'email': 'test@example.com',
                    'password': 'bad',
                    'confirm_password': 'bad'
                }

        res = self.register_user(reg_data)
        # get the results returned in json format
        result = res.data
        # assert that the request contains an error message and a 403 status code
        self.assertIn("Password length should be more than 5 characters, have one lowercase, uppercase, number and special character",  str(result))
        self.assertEqual(res.status_code, 200)

    
     def test_already_registered_user(self):
        """Test that a user cannot be registered twice."""
        reg_data = {
            'username':'bigdolfr',
            'email': 'test@example.com',
            'password': 'J@yd33n',
            'confirm_password': 'J@yd33n'
                }
        self.register_user(self.user_data)
        res = self.register_user(reg_data)
        self.assertEqual(res.status_code, 302)
        # get the results returned in json format
        result = json.loads(res.data.decode())
        self.assertEqual(
        result['message'], "An account with that email already exists!")

     def test_already_existing_username(self):
        """Test if username already exists."""
        reg_data = {
            'username':'bigdolf',
            'email': 'testr@example.com',
            'password': 'J@yd33n',
            'confirm_password': 'J@yd33n'
                }
        self.register_user(self.user_data)
        res = self.register_user(reg_data)
        self.assertEqual(res.status_code, 302)
        # get the results returned in json format
        result = json.loads(res.data.decode())
        # assert that the request contains the error message
        self.assertEqual(result['message'], "An account with that username already exists!")

     def test_registration(self):
        """Test user registration works correcty."""
        res = self.register_user(self.user_data)
        print(res)
        # get the results returned in json format
        result = json.loads(res.data.decode())

        # assert that the request contains a success message and a 201 status code
        self.assertEqual(result['message'], "Successfully created an account. Login to access account")
        self.assertEqual(res.status_code, 201)

     def test_user_login(self):
        """Test registered user can login."""
        
        res = self.register_user(self.user_data)
        self.assertEqual(res.status_code, 201)
        login_res = self.client().post('/api/v2/auth/login', data=json.dumps(self.login_data), content_type='application/json')
        #self.login_user(self.login_data)
        print(login_res)
        # get the results in json format
        result = json.loads(login_res.data.decode())
        # Test that the response contains success message
        self.assertEqual(result['message'], "You logged in successfully.")
        # Assert that the status code is equal to 200
        self.assertEqual(login_res.status_code, 200)
    
     def test_invalid_user_login(self):
        """Test non registered users cannot login."""
        # define a dictionary to represent an unregistered user
        not_a_user = {
            'username': 'notadolh',
            'password': 'J@yd33n'
        }
        # send a POST request to /auth/login with the data above
        res = self.login_user(not_a_user)
        # get the result in json
        result = json.loads(res.data.decode())
        # assert that this response must contain an error message
        # and an error status code 401(Unauthorized)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(result['message'], "Invalid username or password, Please try again")


     def test_successful_pass_editing(self):
        """Test successful password editing."""
        # Create a user
        res = self.register_user(self.user_data2)
        self.assertEqual(res.status_code, 201)
        # Get token        
        header_access_token = self.get_new_token()
        # define a dictionary to represent the new passwords
        edit_password = {
            'new_password': 'J@yd33n',
            'confirm_password': 'J@yd33n'
        }
        # send a PUT request to /api/v2/auth/reset-password with the data above
        res = self.client().put('/api/v2/auth/reset-password', headers=dict(header_access_token=header_access_token),
        data=json.dumps(edit_password), content_type='application/json')
        # get the result in json
        result = json.loads(res.data.decode())

        # assert that this response is successful 
        # and a success status code 200(ok)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(result['message'], "Password changed successfully.")

    
     def test_successful_logout(self):
        """Test if a user can successfully logout"""
        # Get token
        header_access_token = self.get_token()
        # Logout user
        res = self.client().post('/api/v2/auth/logout', headers=dict(header_access_token=header_access_token),
        content_type='application/json')
        self.assertEqual(res.status_code, 200)
        result = json.loads(res.data.decode())
        self.assertIn('Successfully logged out.', result['message'])

    
     def test_repeat_logout(self):
        """Test if a user is prevented to logout twice"""
        # Get token
        header_access_token = self.get_token()        
        # Logout user
        self.client().post('/api/v2/auth/logout', headers=dict(header_access_token=header_access_token),
        content_type='application/json')
        res = self.client().post('/api/v2/auth/logout', headers=dict(header_access_token=header_access_token),
        content_type='application/json')     
        self.assertEqual(res.status_code, 401)
        result = json.loads(res.data.decode())
        self.assertIn('Logged out. Please', result['message'])

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
