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
    if not business_item['business']['business'] or not business_item['business']['location'] or not business_item['business']['category']:
        return "Business, Location or Category details cannot be empty!"
    elif len(business_item['business']['business']) < 5 or not re.match("^[a-zA-Z0-9 _]*$", business_item['business']['business']):
        return "Business name cannot have special characters or numbers or less than five characters"  
    else:
        return business_item

#@business.route('/api/v2/<string:category_id>/business', methods=['POST'])
@business.route('/api/v2/business', methods=['POST'])
@token_required
def create_business(current_user, data):   
    """ Method to create review."""
    business_item = request.get_json()
    business_name = business_item['business']['business']
    business_location = business_item['business']['location']
    business_category = business_item['business']['category']
    #category_item = Category.query.filter_by(id=category_id).first()
    #category_public_id = category_item.id
    new_business = validate_business_name(business_item)
    if new_business is not business_item:
        return jsonify({"error":new_business}), 400
    existing = Business.query.filter_by(business=business_name).first()
    if existing:
        response = {"error" : "A similar business already exists!"}
        return make_response(jsonify(response)), 302    
    try:
        created_business = Business(business=business_name, owner = data['username'], category=business_category, business_location = business_location)
        created_business.save()
        response = jsonify({'message': 'Business created successfully.'})
    except KeyError:
        response = {"error": "There was an error creating the business, please try again"}
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
        business_name = business_item['business']
        business_location = business_item['business_location']
        business_category = business_item['business_category']
       # new_business = validate_business_name(business_item)
       # if new_business is not business_item:
        #    return jsonify({"error":"An error occured please recheck your inputs try again"}), 400
        existing = Business.query.filter_by(business=business_item['business']).first()
        if existing:
            response = {"error" : "A similar business already exists!"}
            return make_response(jsonify(response)), 302 
        try:
            current_business.business = business_name
            current_business.business_location = business_location
            current_business.category = business_category
            current_business.save()
            response = {'message': 'Business updated successfully.'}
            return make_response(jsonify(response)), 200
        except KeyError:
            response = {"error": "There was an error updating the business, please try again"}
            return make_response(jsonify(response)), 500
    response = {"error": "You can only update your own business"}
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
            'business_category': business.category,
            'business_location': business.business_location
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
        response = {"result": "Business {} deleted".format(business.id)}
        return jsonify(response), 200
    response = {"error": "You can only delete your own business"}
    return jsonify(response), 401

@business.route('/api/v2/business/all', methods=['GET'])
@business.route('/api/v2/business/all/page=<int:page>', methods=['GET'])
@business.route('/api/v2/business/all/page=<int:page>&limit=<int:limit>', methods=['GET'])
#@token_required
def get_all_businesses(limit=2, page=1): 

    # businesses = Business.query.paginate(page, per_page = limit, error_out=True).items
    businesses = Business.query.order_by(Business.id.desc()).paginate(page, limit, False).items


    results = []
    for business_item in businesses:
        obj = {
            'business_id': business_item.id,
            'business': business_item.business, 
            'business_owner' : business_item.owner,
            'business_category': business_item.category,
            'business_location': business_item.business_location
                }
        results.append(obj)
    return make_response(jsonify({"businesses":results})), 200

@business.route('/api/v2/<userName>/businesses')
@token_required
def get_current_user_businesses(current_user, data, userName):
    """GET businesses created by current_user."""
    try:
        # get all businesses created by the user currently logged in
        all_businesses = Business.query.order_by(Business.id.desc()).filter_by(owner=userName)
        businesses = []
        print(all_businesses)
        for business in all_businesses:
            business_data = {
            'business_id': business.id,
            'business': business.business, 
            'business_owner' : business.owner,
            'business_category': business.category,
            'business_location': business.business_location
            }
            businesses.append(business_data)
        if businesses:
            return jsonify({'businesses': businesses}), 200
        return jsonify({"message": "You haven't created any businesses"}), 404
    except Exception:
        return make_response(jsonify({"error": "Server error"})), 500

@business.route('/api/v2/search', methods=['GET'])
def search(limit=6, page=1):
    """Search for business in the system"""
    location = request.args.get("location")
    category = request.args.get("category")
    # get q search value and use if available
    q = request.args.get("q")

    if q and location:
        found_businesses = Business.query.filter(Business.business_location.ilike('%{}%'.format(location)), Business.business.ilike('%{}%'.format(q))).paginate(page, per_page = limit, error_out=False).items
        found_business_list = []
        if not found_businesses:
            return jsonify({'message': 'No existing businesses have been found'}), 404
        for business_item in found_businesses:
            available_business = {'business_name': business_item.business, 'business_category_id': business_item.category, 'business_location': business_item.business_location, 'owner':business_item.owner}
            found_business_list.append(available_business)
        return jsonify({'Businesses': found_business_list}), 200 
    elif location:
        location_businesses = Business.query.filter(Business.business_location.ilike('%{}%'.format(location))).paginate(page, per_page = limit, error_out=False).items
        business_list = []
        if not location_businesses:
            return jsonify({'message': 'There are no existing business in this location'}), 404
        for business_item in location_businesses:
            found_business = {'business_name': business_item.business, 'business_category': business_item.category, 'business_location': business_item.business_location, 'owner':business_item.owner}
            business_list.append(found_business)
        return jsonify({'Businesses': business_list}), 200        
    elif q:
        name_business = Business.query.filter(Business.business.ilike('%{}%'.format(q))).paginate(page, per_page = limit, error_out=False).items
        business_list = []
        if not name_business:
            return jsonify({'message': 'No existing businesses'}), 404
        for business_item in name_business:
            found_business = {'business_name': business_item.business, 'business_category': business_item.category, 'business_location': business_item.business_location, 'owner':business_item.owner}
            business_list.append(found_business)
        return jsonify({'Businesses': business_list}), 200
    else:
        return jsonify({'Warning': 'Cannot comprehend the given search parameter'})

		