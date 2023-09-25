#!/usr/bin/python3
"""
This module generates a view for Review objects that handles
all default RESTFul API actions
"""
from flask import Flask, jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.review import Review
from models.place import Place
from models.user import User
import json


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_reviews(place_id):
    """
    Retrieves the list of all rewiew objects

    Returns:
        JSON response: A JSON response containing a list of dictionaries,
        where each dictionary represents a review instance.
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    reviews = [review.to_dict() for review in place.reviews]
    return json.dumps(reviews, indent=4)


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def get_review(review_id):
    """
    Retrieve a Review object based on the provided review_id and return its
    JSON representation.

    Args:
        review_id (str): The ID of the user to retrieve.

    Returns:
        str: JSON representation of the Review object if it exists.
        None: If the state does not exist, aborts the request with a 404 error.
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return json.dumps(review.to_dict(), indent=4)


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """
    Deletes a Review object

    Args:
        review_id (str): The ID of the Review object to be deleted.

    Returns:
        dict: An empty JSON response indicating that the Review object has
        been successfully deleted.
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    review.delete()
    storage.save()
    return jsonify({})


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """
    Create a new review.

    This route handles a POST request to create a new Review.

    :return: JSON response containing the newly created Review object with
    status code 201.
             If there are any errors, it returns a JSON response with
             an error message and status code 400.
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    if 'user_id' not in request.json:
        return jsonify({"error": "Missing user_id"}), 400
    user = storage.get(User, request.json['user_id'])
    if user is None:
        abort(404)
    if 'text' not in request.json:
        return jsonify({"error": "Missing text"}), 400
    review = Review(place_id=place_id, **request.get_json())
    review.save()
    return json.dumps(review.to_dict(), indent=4), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    """
    Update a specific review.

    Args:
        review_id (str): The ID of the review to be updated, extracted
        from the URL.

    Returns:
        dict: A JSON response with a success message if the review exists
        and the request data is valid.
              A JSON response with an error message if the user does not
              exist or the request data is invalid.
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    ignore = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    for key, value in request.get_json().items():
        if key not in ignore:
            setattr(review, key, value)
    review.save()
    return json.dumps(review.to_dict(), indent=4), 200
