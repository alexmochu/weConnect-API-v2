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
- Access the API documentation at "#"

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
- Type:
`export FLASK_CONFIG=developmemt`
`export FLASK_APP=run.py`
`flask run`

# Running the Tests


# API Endpoints

| Resource URL | Methods | Description
|-------------- |------- |---------------
| /api/v2/auth/register | POST | User Registration
| /api/v2/auth/login    | POST | User Login



