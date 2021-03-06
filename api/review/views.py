# api/review/views.py
import re

from flask import jsonify, request, make_response

# local imports
from . import review
from .. import db
from ..models import User, Business, Review
from api.auth.views import token_required

def validate_business_review(review_item):
    if not review_item['review']:
        return "Review cannot be empty!"
    elif len(review_item['review']) < 10 :
        return "Business name cannot have special characters or numbers or less than five characters"  
    else:
        return review_item

@review.route('/api/v2/<business_id>/review', methods=['POST'])
@token_required
def create_review(current_user, data, business_id):
    """ Method to create review."""
    review_item = request.get_json()
    business_review = review_item['review']
    business_item = Business.query.filter_by(id=business_id).first()
    print(business_item)
    if not business_item:
        response = {"error" : "Business does not exist!"}
        return make_response(jsonify(response)), 404 
    new_review = validate_business_review(review_item)
    if new_review is not review_item:
        return jsonify({"error":new_review}), 400
    existing = Review.query.filter_by(reviewer=data['username'], business_id=business_id).first()
    if existing:
        response = {"error" : "You have already reveiwed this business please review another one"}
        return make_response(jsonify(response)), 302  
    try:
        created_review = Review(review=business_review, reviewer=data['username'], business_id=business_item.id)
        created_review.save()
        response = jsonify({
            'review' : created_review.review,
            'reviewer' : created_review.reviewer
        })
    except KeyError:
        response = {"error": "There was an error creating the review, please try again"}
        return make_response(jsonify(response)), 500                            
    return make_response(response), 201

@review.route('/api/v2/reviews/all', methods=['GET'])
@review.route('/api/v2/reviews/all/page=<int:page>', methods=['GET'])
@review.route('/api/v2/reviews/all/page=<int:page>&limit=<int:limit>', methods=['GET'])
def get_all_reviews(limit=4, page=1): 

    reviews = Review.query.paginate(page, per_page = limit, error_out=True).items

    results = []
    for review_item in reviews:
        obj = {
            'review': review_item.review, 'reviewer' : review_item.reviewer, 'business_id': review_item.business_id
                }
        results.append(obj)
    return make_response(jsonify({"reviews":results})), 200

@review.route('/api/v2/<business_id>/reviews')
@token_required
def get_current_business_review(current_user, data, business_id):
    """GET reviews by Business ID"""
    try:
        # get all businesses created by the user currently logged in
        all_reviews = Review.query.filter_by(business_id=business_id).all()
        reviews = []
        for review in all_reviews:
            print(review)
            review_data = {
            'business_id': review.business_id,
            'review': review.review, 
            'reviewer' : review.reviewer
            }
            print(review_data)
            reviews.append(review_data)
            print("============", reviews)
        if reviews:
            
            return jsonify({'reviews': reviews}), 200
        return jsonify({"message": "You haven't created any reviews"}), 404
    except Exception:
        return make_response(jsonify({"error": "Server error"})), 500