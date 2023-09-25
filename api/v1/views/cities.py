#!/usr/bin/python3
"""This script defines a Flask view function for the API."""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.state import State
from models.city import City
import json


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities_of_state(state_id):
    """
    Retrieves all instances of the City class from the database and returns
    them as a JSON response.

    Returns:
        JSON response: A JSON response containing a list of dictionaries,
        where each dictionary represents a state instance.
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    cities = [city.to_dict() for city in state.cities]

    return json.dumps(cities, indent=4)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """
    Retrieve a City object based on the provided city_id and return its
    JSON representation.

    Args:
        city_id (str): The ID of the city to retrieve.

    Returns:
        str: JSON representation of the City object if it exists.
        None: If the state does not exist, aborts the request with a 404 error.
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return json.dumps(city.to_dict(), indent=4)


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """
    Delete a City object.

    Args:
        city_id (str): The ID of the city object to be deleted.

    Returns:
        dict: An empty JSON response indicating that the City object has
        been successfully deleted.
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    city.delete()
    storage.save()
    return jsonify({})


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """
    Create a new city.

    This route handles a POST request to create a new city.

    :return: JSON response containing the newly created city object with
    status code 201.
             If there are any errors, it returns a JSON response with
             an error message and status code 400.
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    if 'name' not in request.json:
        return jsonify({"error": "Missing name"}), 400
    city = City(state_id=state_id, **request.get_json())
    city.save()
    return json.dumps(city.to_dict(), indent=4), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """
    Update a specific city.

    Args:
        city_id (str): The ID of the city to be updated, extracted
        from the URL.

    Returns:
        dict: A JSON response with a success message if the city exists
        and the request data is valid.
              A JSON response with an error message if the city does not
              exist or the request data is invalid.
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400

    ignore = ['id', 'state_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore:
            setattr(city, key, value)

    city.save()
    return json.dumps(city.to_dict(), indent=4), 200
