#!/usr/bin/python3
"""
This code snippet defines several Flask routes for handling
HTTP requests related to places.

Example Usage:
- GET request to retrieve all places in a city:
    GET /cities/<city_id>/places
    Response: JSON representation of a list of places

- GET request to retrieve a specific place:
    GET /places/<place_id>
    Response: JSON representation of the place

- DELETE request to delete a specific place:
    DELETE /places/<place_id>
    Response: Empty JSON object

- POST request to create a new place in a city:
    POST /cities/<city_id>/places
    Request body: JSON representation of the new place
    Response: JSON representation of the created place

- PUT request to update a specific place:
    PUT /places/<place_id>
    Request body: JSON representation of the updated place attributes
    Response: JSON representation of the updated place

Inputs:
- city_id: a string representing the ID of the city
- place_id: a string representing the ID of the place
- params: a dictionary containing the request body parameters

Outputs:
- JSON responses containing the requested or modified place details,
or an empty response

"""

from flask import jsonify, abort, request
from models.place import Place
from models.city import City
from models.user import User
from models import storage
from api.v1.views import app_views


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    """
    Retrieve all places in a city.

    Args:
        city_id (str): The ID of the city.

    Returns:
        JSON response: A JSON representation of a list of places.

    Raises:
        404: If no city with the provided city_id is found.
    """
    for city in storage.all(City).values():
        if city.id == city_id:
            list_places = []
            for place in city.places:
                list_places.append(place.to_dict())
            return jsonify(list_places)
    return abort(404)


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def get_place(place_id):
    """
    Retrieve a specific place.

    Args:
        place_id (str): The ID of the place.

    Returns:
        JSON response: A JSON representation of the place.

    Raises:
        404: If no place with the provided place_id is found.
    """
    place = storage.get(Place, place_id)
    if place is None:
        return abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """
    Delete a specific place.

    Args:
        place_id (str): The ID of the place.

    Returns:
        JSON response: An empty JSON object.

    Raises:
        404: If no place with the provided place_id is found.
    """
    place = storage.get(Place, place_id)
    if place is None:
        return abort(404)
    place.delete()
    storage.save()
    return jsonify({})


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def post_place(city_id):
    """
    Create a new place in a city.

    Args:
        city_id (str): The ID of the city.

    Returns:
        JSON response: A JSON representation of the created place.

    Raises:
        404: If no city with the provided city_id is found.
        400: If the request body is not a valid JSON or is missing
        required parameters.
    """
    city = storage.get(City, city_id)
    if city is None:
        return abort(404)
    params = request.get_json()
    if params is None:
        abort(400, "Not a JSON")
    if params.get("user_id") is None:
        abort(400, "Missing user_id")
    user = storage.get(User, params['user_id'])
    if user is None:
        return abort(404)
    if params.get("name") is None:
        abort(400, "Missing name")
    params['city_id'] = city_id
    new = Place(**params)
    new.save()
    return jsonify(new.to_dict()), 201


@app_views.route('/places/<place_id>',
                 methods=['PUT'], strict_slashes=False)
def put_place(place_id):
    """
    Update a specific place.

    Args:
        place_id (str): The ID of the place.

    Returns:
        JSON response: A JSON representation of the updated place.

    Raises:
        404: If no place with the provided place_id is found.
        400: If the request body is not a valid JSON.
    """
    place = storage.get(Place, place_id)
    if place is None:
        return abort(404)
    params = request.get_json()
    if params is None:
        return abort(400, "Not a JSON")
    li = ["id", "created_at", "updated_at", "user_id"]
    for key, value in params.items():
        if key not in li:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict())
