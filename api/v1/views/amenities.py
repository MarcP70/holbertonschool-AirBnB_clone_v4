#!/usr/bin/python3
"""
This code snippet defines several Flask routes for handling
CRUD operations on the Amenity model.

The available routes are:
- GET /amenities: Retrieve all amenities from the database and
return a JSON response.
- GET /amenities/<amenity_id>: Retrieve the details of a specific
amenity identified by its ID and return a JSON response.
- DELETE /amenities/<amenity_id>: Delete an Amenity object from the storage.
- POST /amenities: Create a new Amenity object using the data from the
request body and return a JSON response.
- PUT /amenities/<amenity_id>: Update an existing Amenity object with the
specified ID using the data from the request body and return a JSON response.

Each route has its own function with a docstring explaining its purpose,
inputs, and outputs.

Example usage and expected responses are provided in the code explanation.

Note: The code snippet assumes the existence of the necessary imports and
the Flask app_views blueprint.
"""


from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.amenity import Amenity
import json


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenites():
    """
    Retrieve all amenities from the database and return a JSON response.

    Returns:
        str: JSON response containing all amenities.
    """
    amenities = storage.all(Amenity).values()
    return json.dumps([amenity.to_dict() for amenity in amenities], indent=4)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """
    Retrieve the details of a specific amenity identified by its ID
    and return a JSON response.

    Args:
        amenity_id (str): The ID of the amenity.

    Returns:
        str: JSON response containing the details of the specified
        amenity.

    Raises:
        404: If the amenity does not exist.
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        return jsonify(amenity.to_dict())
    abort(404)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """
    Delete an Amenity object from the storage.

    Args:
        amenity_id (str): The ID of the Amenity object to be deleted.

    Returns:
        dict: An empty JSON response.

    Raises:
        404: If the Amenity object does not exist.
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        return jsonify({'error': 'Amenity not found'}), 404
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """
    Create a new Amenity object.

    This function handles a POST request to create a new Amenity object.

    :return: JSON response with the details of the created Amenity
    and status code.
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    if "name" not in data:
        return jsonify({"error": "Missing name"}), 400
    new_amenity = Amenity(**data)
    new_amenity.save()
    return json.dumps(new_amenity.to_dict(), indent=4), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """
    Update an Amenity object with the specified ID.

    Args:
        amenity_id (str): The ID of the Amenity object to be updated.

    Returns:
        str: JSON response containing the updated Amenity object if
        it exists, or an error message if it does not exist.

    Example Usage:
        # Request:
        # POST /amenities/1
        # Request Body:
        # {
        #   "name": "New Amenity Name"
        # }
        # Response:
        # {
        #   "id": 1,
        #   "name": "New Amenity Name",
        #   "created_at": "2021-01-01T00:00:00",
        #   "updated_at": "2021-01-02T00:00:00"
        # }

        # The code above is used to update an existing Amenity object
        with the specified ID. The new name is provided in the request
        body. The response contains the updated Amenity object in JSON format.
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Not a JSON"}), 400
        for key, value in data.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(amenity, key, value)
        amenity.save()
        return jsonify(amenity.to_dict())
    abort(404)
