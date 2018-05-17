# api/categ/views.py
import re
import uuid

from flask import jsonify, request, make_response
from functools import wraps

# local imports
from . import category
from .. import db
from ..models import User, Category
from api.auth.views import token_required

def validate_data(category_item):
    if not category_item['category_name']:
        return "Category details cannot be empty!"
    elif len(category_item['category_name']) < 5 or not re.match("^[a-zA-Z0-9 _]*$", category_item['category_name']):
        return "Category name cannot have special characters or numbers or less than 5 characters"  
    else:
        return category_item

@category.route('/api/v2/category', methods=['POST'])
@token_required
def create_category(current_user, data):
    """ Method to create event."""
    category_item = request.get_json()
    category_name = category_item['category_name']
    new_category = validate_data(category_item)
    if new_category is not category_item:
        return jsonify({"message":"An error occured please recheck your inputs try again"}), 400
    existing = Category.query.filter_by(category=category_name).first()
    if existing:
        response = {"message" : "A similar category already exists!"}
        return make_response(jsonify(response)), 302    
    try:
        created_category = Category(category=category_name, created_by = data['username'])
        created_category.save()
        response = jsonify({
            'category_id': created_category.id,
            'category_name' : created_category.category,
            'created_by' : created_category.created_by
        })
    except KeyError:
        response = {"message": "There was an error creating the category, please try again"}
        return make_response(jsonify(response)), 500                            
    return make_response(response), 201

@category.route('/api/v2/category/all', methods=['GET'])
@category.route('/api/v2/category/all/page=<int:page>', methods=['GET'])
@category.route('/api/v2/category/all/page=<int:page>&limit=<int:limit>', methods=['GET'])
def get_all_categories(limit=4, page=1):

    categories = Category.query.paginate(page, per_page = limit, error_out=True).items
    results = []
    for category_item in categories:
        obj = {
            'category_id': category_item.id,
            'category_name': category_item.category, 
            'category_owner' : category_item.created_by
                }
        results.append(obj)
    return make_response(jsonify(results)), 200

@category.route('/api/v2/category/<category_id>', methods=['PUT'])
@token_required
def update_category(current_user, data, category_id):
    current_category = Category.query.filter_by(id=category_id).first()
    created_by = current_category.created_by
    if data['username'] == created_by:
    # Obtain the new name of the category from the request data
        category_item = request.get_json()
        new_category = validate_data(category_item)
        if new_category is not category_item:
            return jsonify({"message":"An error occured please recheck your inputs try again"}), 400
        existing = Category.query.filter_by(category=new_category['category_name']).first()
        if existing:
            response = {"message" : "A similar category already exists!"}
            return make_response(jsonify(response)), 302 
        try:
            current_category.category = new_category['category_name']
            current_category.save()
            response = {      
                'category_id': current_category.id,
                'category_name': current_category.category, 
                'category_owner' : current_category.created_by
                }
            return make_response(jsonify(response)), 200
        except KeyError:
            response = {"message": "There was an error updating the category, please try again"}
            return make_response(jsonify(response)), 500
    response = {"message": "You can only update your own category"}
    return jsonify(response), 401

@category.route('/api/v2/category/<category_id>', methods=['DELETE'])
@token_required
def delete_category_by_id(current_user, data, category_id):
    """ Method to get business by ID """
    category = Category.query.filter_by(id=category_id).first()
    
    created_by = category.created_by
    if data['username'] == created_by:
        category.delete()
        response = {"message": "Category {} deleted".format(category.id)}
        return jsonify(response), 200
    response = {"message": "You can only delete your own business"}
    return jsonify(response), 401