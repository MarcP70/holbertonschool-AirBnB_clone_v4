#!/usr/bin/python3
"""This script defines a Flask view function for the API."""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route("/status")
def status():
    """Provides a route to check the status of the API."""
    return jsonify(status="OK")


@app_views.route('/stats', methods=['GET'])
def stats():
    classes = {
        "amenities": Amenity,
        "cities": City,
        "places": Place,
        "reviews": Review,
        "states": State,
        "users": User
    }
    stats_dict = {}
    for key, class_name in classes.items():
        stats_dict[key] = storage.count(class_name)

    return jsonify(stats_dict)
