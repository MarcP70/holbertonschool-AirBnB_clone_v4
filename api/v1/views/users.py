#!/usr/bin/python3
"""
This module generates a view for User objects that
handles all default RESTFul API actions
"""
from flask import Flask, jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.user import User
import json


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """
    Retrieves the list of all User objects

    Returns:
        JSON response: A JSON response containing a list of dictionaries,
        where each dictionary represents a user instance.
    """
    users = storage.all(User).values()
    return json.dumps([user.to_dict() for user in users], indent=4)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """
    Retrieve a User object based on the provided user_id and return its
    JSON representation.

    Args:
        user_id (str): The ID of the user to retrieve.

    Returns:
        str: JSON representation of the User object if it exists.
        None: If the state does not exist, aborts the request with a 404 error.
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return json.dumps(user.to_dict(), indent=4)


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """
    Deletes a User object

    Args:
        user_id (str): The ID of the User object to be deleted.

    Returns:
        dict: An empty JSON response indicating that the User object has
        been successfully deleted.
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    user.delete()
    storage.save()
    return jsonify({})


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """
    Create a new user.

    This route handles a POST request to create a new User.

    :return: JSON response containing the newly created User object with
    status code 201.
             If there are any errors, it returns a JSON response with
             an error message and status code 400.
    """
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    if 'email' not in request.json:
        return jsonify({"error": "Missing email"}), 400
    if 'password' not in request.json:
        return jsonify({"error": "Missing password"}), 400
    user = User(**request.get_json())
    user.save()
    return json.dumps(user.to_dict(), indent=4), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """
    Update a specific user.

    Args:
        user_id (str): The ID of the user to be updated, extracted
        from the URL.

    Returns:
        dict: A JSON response with a success message if the user exists
        and the request data is valid.
              A JSON response with an error message if the user does not
              exist or the request data is invalid.
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    ignore = ['id', 'email', 'created_at', 'updated_at']
    for key, value in request.get_json().items():
        if key not in ignore:
            setattr(user, key, value)
    user.save()
    return json.dumps(user.to_dict()), 200
