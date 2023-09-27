#!/usr/bin/python3
""" Starts a Flash Web Application """
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from os import environ
from flask import Flask, render_template, jsonify, request
import uuid
app = Flask(__name__)
# app.jinja_env.trim_blocks = True
# app.jinja_env.lstrip_blocks = True


@app.teardown_appcontext
def close_db(error):
    """ Remove the current SQLAlchemy Session """
    storage.close()


@app.route('/4-hbnb/', methods=['GET', 'POST'], strict_slashes=False)
def hbnb():
    """ HBNB is alive! """
    if request.method == 'POST':
        # For POST request, handle places_search with amenities
        amenities = request.get_json().get('amenities', [])
        filtered_places = get_filtered_places(amenities)
        return jsonify([place.to_dict() for place in filtered_places])

    # For GET request, render the template with data
    states = storage.all(State).values()
    states = sorted(states, key=lambda k: k.name)
    st_ct = []

    for state in states:
        st_ct.append([state, sorted(state.cities, key=lambda k: k.name)])

    amenities = storage.all(Amenity).values()
    amenities = sorted(amenities, key=lambda k: k.name)

    places = storage.all(Place).values()
    places = sorted(places, key=lambda k: k.name)

    cache_id = str(uuid.uuid4())

    return render_template('4-hbnb.html',
                           states=st_ct,
                           amenities=amenities,
                           places=places,
                           cache_id=cache_id
                           )


def get_filtered_places(amenities):
    """ Filter places based on amenities """
    if not amenities:
        return storage.all(Place).values()

    filtered_places = set()
    for amenity_id in amenities:
        amenity = storage.get(Amenity, amenity_id)
        if amenity:
            for place in amenity.places:
                filtered_places.add(place)

    return list(filtered_places)


@app.route('/api/v1/places_search/', methods=['POST'])
def places_search():
    """ Search for places """
    data = request.get_json()

    places = storage.all(Place).values()
    places = sorted(places, key=lambda k: k.name)

    places_list = []
    for place in places:
        places_list.append(place.to_dict())

    return jsonify(places_list)

if __name__ == "__main__":
    """ Main Function """
    app.run(host='0.0.0.0', port=5000)
