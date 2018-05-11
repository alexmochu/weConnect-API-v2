# api/categ/views.py
import re

from flask import jsonify, request, make_response
from functools import wraps

# local imports
from . import categ
from .. import db
from ..models import User, Category
from api.auth.views import token_required

def validate_data(category_item):
    if not category_item['category'] or not category_item['description']:
        return "Category details cannot be empty!"
    elif len(category_item['category']) < 5 or not re.match("^[a-zA-Z0-9 _]*$", category_item['category']):
        return "Category name cannot have special characters or numbers or less than 5 characters"  
    else:
        return category_item

@categ.route('/api/v2/category', methods=['POST'])
@token_required
def create_category(current_user, data):
    """ Method to create event."""
    category_item = request.get_json()
    category_name = category_item['category']
    category_description = category_item['description']
    new_category = validate_data(category_item)
    if new_category is not category_item:
        return jsonify({"message":new_category}), 400
    existing = Category.query.filter_by(category=category_name).first()
    if existing:
        response = {"message" : "A similar category already exists!"}
        return make_response(jsonify(response)), 302    
    try:
        created_category = Category(category=category_name, description=category_description, created_by = data['username'])
        created_category.save()
        response = jsonify({
            'category' : created_category.category,
            'category_description' : created_category.description, 'created_by' : created_category.created_by
        })
    except KeyError:
        response = {"message": "There was an error creating the category, please try again"}
        return make_response(jsonify(response)), 500                            
    return make_response(response), 201

@categ.route('/api/v2/category', methods=['GET'])
def get_all_categories():

    categories = Category.query.all()

    results = []
    for category_item in categories:
        obj = {
            'category': category_item.category, 'username' : category_item.created_by, 'category_description' : category_item.description
                }
        results.append(obj)
    return make_response(jsonify(results)), 200