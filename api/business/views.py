# api/business/views.py
import re

from flask import jsonify, request, make_response

# local imports
from . import business
from .. import db
from ..models import User, Category, Business
from api.auth.views import token_required

def validate_business_name(business_item):
    if not business_item['business'] or not business_item['description']:
        return "Business details cannot be empty!"
    elif len(business_item['business']) < 5 or not re.match("^[a-zA-Z0-9 _]*$", business_item['business']):
        return "Business name cannot have special characters or numbers or less than five characters"  
    else:
        return business_item

@business.route('/api/v2/<category>/business', methods=['POST'])
@token_required
def create_business(current_user, data, category):
    """ Method to create review."""
    business_item = request.get_json()
    business_name = business_item['business']
    description = business_item['description']
    category_item = Category.query.filter_by(category=category).first()
    if not category_item:
        response = {"message" : "Category does not exist!"}
        return make_response(jsonify(response)), 404 
    new_business = validate_business_name(business_item)
    if new_business is not business_item:
        return jsonify({"message":new_business}), 400
    existing = Business.query.filter_by(business=business_name).first()
    if existing:
        response = {"message" : "A similar business already exists!"}
        return make_response(jsonify(response)), 302    
    try:
        created_business = Business(business=business_name, biz_description=description, owner = data['username'], business_categ_id=category_item.id)
        created_business.save()
        response = jsonify({
            'business' : created_business.business,
            'description' : created_business.biz_description, 
            'owner' : created_business.owner
        })
    except KeyError:
        response = {"message": "There was an error creating the business, please try again"}
        return make_response(jsonify(response)), 500                            
    return make_response(response), 201

@business.route('/api/v2/business', methods=['GET'])
def get_all_businesses(): 

    businesses = Business.query.all()

    results = []
    for business_item in businesses:
        obj = {
            'business': business_item.business, 'owner' : business_item.owner, 'business_description' : business_item.biz_description
                }
        results.append(obj)
    return make_response(jsonify(results)), 200