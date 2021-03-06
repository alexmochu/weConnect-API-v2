[![Codacy Badge](https://api.codacy.com/project/badge/Grade/d2bb80729b76446e85540300e4af348d)](https://www.codacy.com/app/alexmochu/weConnect-API-v2?utm_source=github.com&utm_medium=referral&utm_content=alexmochu/weConnect-API-v2&utm_campaign=Badge_Grade)
[![Maintainability](https://api.codeclimate.com/v1/badges/d5c2e3a5f81cba46d514/maintainability)](https://codeclimate.com/github/alexmochu/weConnect-API-v2/maintainability)
[![Build Status](https://travis-ci.org/alexmochu/weConnect-API-v2.svg?branch=master)](https://travis-ci.org/alexmochu/weConnect-API-v2)
[![Coverage Status](https://coveralls.io/repos/github/alexmochu/weConnect-API-v2/badge.svg?branch=master)](https://coveralls.io/github/alexmochu/weConnect-API-v2?branch=master)

# weConnect-API-v2

WeConnect provides a platform that brings businesses and individuals together. This platform creates awareness for businesses and gives the users the ability to write reviews about the businesses they have interacted with.

# Technology Used

The API has been built with:

- Flask micro-framework (Python 3.6)
- Postgresql Database
- JSON Web Tokens

# UI templates and API Documentation

- To preview the UI, proceed to https://alexmochu.github.io .
- The <a href="https://github.com/alexmochu/alexmochu.github.io">UI Templates</a> have been hosted on Github Pages
- To access the API hosted on the Heroku cloud platform -->> https://weconnect-v2-heroku.herokuapp.com/
- Access the API documentation at "https://weconnectv2.docs.apiary.io"

# Features

1.  Users can be able to register and create an account
2.  Registered users can be able to log in

# Installation

1. Ensure you have installed Python3.6+, created and an activated a virtual environment.
2. Clone the repo in your local machine inside the virtual environment you have created.
3. Navigate to the project folder(WeConnect-API-v2)
4. Install all the requirements of the project by typing:
   `pip install -r requirements.txt`

# Running the API

## Make Migrations
- Create this folder and file inside the main folder `/instance/config.py` add this two lines 

`SECRET_KEY = 'your_secret_key_here'` 
`SQLALCHEMY_DATABASE_URI = 'your_postgres_database_uri'`

- Type in terminal:
`flask db init`
`flask db migrate`
`flask db upgrade`

- NOTE: While on development uncomment line 20 and comment line 19 `/app/__init__.py` file. Reverse this while on production.

- Type in terminal:
  `export FLASK_CONFIG=developmemt`
  `export FLASK_APP=run.py`
  `flask run`

# Running the Tests

# API Endpoints

| Resource URL                                          | Methods | Description                                        |
| ----------------------------------------------------- | ------- | -------------------------------------------------- |
| /api/v2/auth/register                                 | POST    | User Registration                                  |
| /api/v2/auth/login                                    | POST    | User Login                                         |
| /api/v2/auth/reset-password                           | PUT     | User can be able to reset password                 |
| /api/v2/auth/logout                                   | DELETE  | Logs out User                                      |
| /api/v2/category                                      | POST    | Create a business category                         |
| /api/v2/category/all                                  | GET     | Retrieve all created categories                    |
| /api/v2/category/<category_id>                        | PUT     | Updates a business category                        |
| /api/v2/category/<category_id>                        | DELETE  | Deletes a business category                        |
| /api/v2/<category_id>/business                        | POST    | Create a business with unique ID and business name |
| /api/v2/business/all                                  | GET     | Retrive all business created                       |
| /api/v2/business/<business_id>                        | GET     | Retrive a business by ID                           |
| /api/v2/business/<business_id>                        | DELETE  | Remove a business                                  |
| /api/v2/<business_id>/review                          | POST    | Add a review for a business                        |
| /api/v2/reviews/all                                   | GET     | Get all reviews                                    |
| /api/v2/reviews/all/page=<int:page>                   | GET     | (Paginantion)Get all reviews                       |
| /api/v2/reviews/all/page=<int:page>&limit=<int:limit> | GET     | (Paginantion)Get all reviews                       |

# Pagination

| Resource URL                                           | Methods | Description                                  |
| ------------------------------------------------------ | ------- | -------------------------------------------- |
| /api/v2/category/all/page=<int:page>                   | GET     | (Paginantion)Retrieve all created categories |
| /api/v2/category/all/page=<int:page>&limit=<int:limit> | GET     | (Paginantion)Retrieve all created categories |
| /api/v2/business/all/page=<int:page>                   | GET     | (Paginantion)Retrive all business created    |
| /api/v2/business/all/page=<int:page>&limit=<int:limit> | GET     | (Paginantion)Retrive all business created    |

# Searching

| Resource URL                | Methods | Description          |
| --------------------------- | ------- | -------------------- |
| /api/v2/search?q=<business> | GET     | Search Business by q |

# Searching and Filtering

| Resource URL                                                        | Methods | Description                              |
| ------------------------------------------------------------------- | ------- | ---------------------------------------- |
| /api/v2/search?q=<business>&location=<location>&category=<category> | GET     | Filter Business by Location and Category |
