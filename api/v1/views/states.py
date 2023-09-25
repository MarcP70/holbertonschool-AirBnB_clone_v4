#!/usr/bin/python3
"""This script defines a Flask view function for the API."""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.state import State
import json


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """
    Retrieves all instances of the State class from the database and returns
    them as a JSON response.

    Returns:
        JSON response: A JSON response containing a list of dictionaries,
        where each dictionary represents a state instance.
    """
    states = storage.all(State).values()
    return json.dumps([state.to_dict() for state in states], indent=4)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """
    Retrieve a State object based on the provided state_id and return its
    JSON representation.

    Args:
        state_id (str): The ID of the state to retrieve.

    Returns:
        str: JSON representation of the State object if it exists.
        None: If the state does not exist, aborts the request with a 404 error.
    """
    state = storage.get(State, state_id)
    if state:
        return json.dumps(state.to_dict(), indent=4)
    abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """
    Delete a state object.

    Args:
        state_id (str): The ID of the state object to be deleted.

    Returns:
        dict: An empty JSON response indicating that the state object has
        been successfully deleted.
    """
    state = storage.get(State, state_id)
    if state:
        storage.delete(state)
        storage.save()
        return jsonify({})
    abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """
    Create a new state.

    This route handles a POST request to create a new state.

    :return: JSON response containing the newly created state object with
    status code 201.
             If there are any errors, it returns a JSON response with
             an error message and status code 400.
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    if "name" not in data:
        return jsonify({"error": "Missing name"}), 400
    new_state = State(**data)
    new_state.save()
    return json.dumps(new_state.to_dict(), indent=4), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """
    Update a specific state.

    Args:
        state_id (str): The ID of the state to be updated, extracted
        from the URL.

    Returns:
        dict: A JSON response with a success message if the state exists
        and the request data is valid.
              A JSON response with an error message if the state does not
              exist or the request data is invalid.
    """
    state = storage.get(State, state_id)
    if state:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Not a JSON"}), 400
        for key, value in data.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(state, key, value)
        state.save()
        return json.dumps(state.to_dict(), indent=4)
    abort(404)
