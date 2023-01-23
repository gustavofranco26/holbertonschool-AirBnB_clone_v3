#!/usr/bin/python3
"""
The script that start a Flask web application with all methods default
"""
from models.review import Review
from models.place import Place
from models.user import User
from models import storage
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request, make_response
import os


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_reviews(place_id=None):
    """
    Retrieves the list of all Place objects
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    reviews_list = []
    for review in place.reviews:
        reviews_list.append(review.to_dict())
    return jsonify(reviews_list)


@app_views.route('/reviews/<review_id>/', methods=['GET'],
                 strict_slashes=False)
def get_review(review_id):
    """
    Retrieves a specific city based on id
    """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """
    Deletes a review object based on id provided
    """
    review = storage.get(Review, review_id)

    if not review:
        abort(404)
    storage.delete(review)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def post_review(place_id):
    """
    Creates a Reviews object
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'text' not in request.get_json():
        abort(400, description="Missing text")
    if 'user_id' not in request.get_json():
        abort(400, description="Missing user_id")

    data = request.get_json()
    user = storage.get(User, data["user_id"])
    if not user:
        abort(404)
    instance = Review(**data)
    instance.place_id = place.id
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def put_review(review_id):
    """
    Updates a Reviews
    """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore = ['id', 'place_id', 'created_at', 'updated_at']

    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(review, key, value)
    storage.save()
    return make_response(jsonify(review.to_dict()), 200)
