# api/business/views.py
import re
import uuid

from flask import jsonify, request, make_response

# local imports
from . import business
from .. import db
from ..models import User, Category, Business
from api.auth.views import token_required

def validate_business_name(business_item):
    if not business_item['business']:
        return "Business details cannot be empty!"
    elif len(business_item['business']) < 5 or not re.match("^[a-zA-Z0-9 _]*$", business_item['business']):
        return "Business name cannot have special characters or numbers or less than five characters"  
    else:
        return business_item

@business.route('/api/v2/<string:category_id>/business', methods=['POST'])
@token_required
def create_business(current_user, data, category_id):
    """ Method to create review."""
    business_item = request.get_json()
    business_name = business_item['business']
    business_location = business_item['location']
    category_item = Category.query.filter_by(id=category_id).first()
    category_public_id = category_item.id
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
        created_business = Business(business=business_name, owner = data['username'], business_category_id=category_id, business_location = business_location)
        created_business.save()
        response = jsonify({
            'business_id': created_business.id,
            'business' : created_business.business,
            'business_category_id': created_business.business_category_id,
            'business_owner' : created_business.owner,
            'business_location' : created_business.business_location
        })
    except KeyError:
        response = {"message": "There was an error creating the business, please try again"}
        return make_response(jsonify(response)), 500                            
    return make_response(response), 201

@business.route('/api/v2/business/<business_id>', methods=['PUT'])
@token_required
def update_business(current_user, data, business_id):
    current_business = Business.query.filter_by(id=business_id).first()
    owner = current_business.owner
    if data['username'] == owner:
    # Obtain the new name of the business from the request data
        business_item = request.get_json()
        new_business = validate_business_name(business_item)
        if new_business is not business_item:
            return jsonify({"message":"An error occured please recheck your inputs try again"}), 400
        existing = Business.query.filter_by(business=new_business['business']).first()
        if existing:
            response = {"message" : "A similar business already exists!"}
            return make_response(jsonify(response)), 302 
        try:
            current_business.business = new_business['business']
            current_business.business_location = new_business['location']
            current_business.save()
            response = {      
                'business_id': current_business.id,
                'business_name': current_business.business,
                'business_location': current_business.business_location, 
                'business_owner' : current_business.owner
                }
            return make_response(jsonify(response)), 200
        except KeyError:
            response = {"message": "There was an error updating the business, please try again"}
            return make_response(jsonify(response)), 500
    response = {"message": "You can only update your own business"}
    return jsonify(response), 401

@business.route('/api/v2/business/<business_id>', methods=['GET'])
@token_required
def get_business_by_id(current_user, data, business_id):
    """ Method to get business by ID """
    business = Business.query.filter_by(id=business_id).first()
    response = {
            'business_id': business.id,
            'business': business.business, 
            'business_owner' : business.owner,
            'business_category_id': business.business_category_id
    }
    return make_response(jsonify({"business":response})), 200

@business.route('/api/v2/business/<business_id>', methods=['DELETE'])
@token_required
def delete_business_by_id(current_user, data, business_id):
    """ Method to get business by ID """
    business = Business.query.filter_by(id=business_id).first()
    
    owner = business.owner
    if data['username'] == owner:
        business.delete()
        response = {"message": "Business {} deleted".format(business.id)}
        return jsonify(response), 200
    response = {"message": "You can only delete your own business"}
    return jsonify(response), 401

@business.route('/api/v2/business/all', methods=['GET'])
@business.route('/api/v2/business/all/page=<int:page>', methods=['GET'])
@business.route('/api/v2/business/all/page=<int:page>&limit=<int:limit>', methods=['GET'])
#@token_required
def get_all_businesses(limit=6, page=1): 

    # businesses = Business.query.paginate(page, per_page = limit, error_out=True).items
    businesses = Business.query.paginate(page, limit, False).items


    results = []
    for business_item in businesses:
        obj = {
            'business_id': business_item.id,
            'business': business_item.business, 
            'business_owner' : business_item.owner,
            'business_category_id': business_item.business_category_id,
            'business_location': business_item.business_location
                }
        results.append(obj)
    return make_response(jsonify({"businesses":results})), 200

@business.route('/api/v2/search', methods=['GET'])
def search():
    """Search for business in the system"""
    location = request.args.get("location")
    # get q search value and use if available
    q = request.args.get("q")
        
    if location:
        location_businesses = Business.query.filter(Business.business_location.ilike('%{}%'.format(location)))
        business_list = []
        if not location_businesses:
            return jsonify({'message': 'There are no existing business in this location'}), 404
        for business_item in location_businesses:
            found_business = {'business_name': business_item.business, 'category_id': business_item.business_category_id, 'location': business_item.business_location, 'owner':business_item.owner}
            business_list.append(found_business)
        return jsonify({'Existing Businesses in this location': business_list}), 200        
    elif q:
        name_business = Business.query.filter(Business.business.ilike('%{}%'.format(q)))\
        .paginate(page, per_page = limit, error_out=False).items
        business_list = []
        if not name_business:
            return jsonify({'message': 'No existing businesses'}), 404
        for business_item in name_business:
            found_business = {'business_name': business_item.business, 'business_category': business_item.business_category_id, 'business_location': business_item.business_location, 'owner':business_item.owner}
            business_list.append(found_business)
        return jsonify({'Existing Businesses': business_list}), 200
    else:
        return jsonify({'Warning': 'Cannot comprehend the given search parameter'})
