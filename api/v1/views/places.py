#!/usr/bin/python3
"""
Route Places
"""

from api.v1.views import app_views, Place, City, User
from flask import jsonify, abort, request
from models import storage


@app_views.route('/cities/<id>/places', strict_slashes=False, methods=['GET'])
def get_city_place(id):
    """Returns place by id"""
    """ Method for the "/cities/<id>/places" path GET
    Returns all Place objects in a City
    ---
    tags:
      - Place
    responses:
      200:
        description: A list of all Place objects
        examples:
          [
            {
              "__class__":"Place",
              "city_id":"1da255c0-f023-4779-8134-2b1b40f87683",
              "created_at":"2017-03-25T02:17:06.000000",
              "description":"The guest house is located uptown two blocks from Tulane U. The house is located in a very safe and convenient location. The house has a private entrance and patio space. The house also has access to a large backyard with a charcoal grill which is shared. This is a simple, clean and affordable place to stay while visiting New Orleans. We provide everything travelers need. Please contact me if you have any questions.<BR />Thanks,<BR />Ryan<BR /><BR />Note: We have a $50 pet fee",
              "id":"279b355e-ff9a-4b85-8114-6db7ad2a4cd2",
              "latitude":29.9493,
              "longitude":-90.1171,
              "max_guest":2,
              "name":"Guest House by Tulane",
              "number_bathrooms":1,
              "number_rooms":0,
              "price_by_night":60,
              "updated_at":"2017-03-25T02:17:06.000000",
              "user_id":"8394fd35-8a8a-479f-a398-48f53b4a6554"
            },
            {
              "__class__":"Place",
              "city_id":"1da255c0-f023-4779-8134-2b1b40f87683",
              "created_at":"2017-03-25T02:17:06.000000",
              "description":"Semi-private room in a cute and cozy shotgun house in the Marigny. 15 minute walk to the French Quarter, 12 minutes to Frenchmen St., 2 minutes to the Bywater. Located around the corner from a few restaurants, bars, a coffee shop, and grocery store.<BR /><BR />The house is a classic shotgun, a very common style of architecture for homes here in New Orleans. We rent three rooms in our house (see our profile for links to the other rooms). Each room is arranged one behind the other. You will be walking through all of our bedrooms to get to your room, and while you'll have your room to yourself, people will need to walk through it to access the kitchen, other bedrooms, backyard, and bathroom. Please look through our photos to see the \"blueprints\" of our house, this will give you an idea to how it's laid out.<BR /><BR />Your room is the third room in the house. It comes furnished with a built in bed, curtain for privacy, XL twin mattress, reading lamp, a chair, vanity with a large mirror,",
              "id":"ffcc9c22-759e-4418-b788-81eda89c2865",
              "latitude":29.9666,
              "longitude":-90.0519,
              "max_guest":1,
              "name":"Affordable room in the Marigny",
              "number_bathrooms":1,
              "number_rooms":1,
              "price_by_night":40,
              "updated_at":"2017-03-25T02:17:06.000000",
              "user_id":"7771bbe9-92ab-46d1-a636-864526361d7d"
            }
          ]
      404:
        description: When data not found
    """
    city = storage.get(City, id)
    if city:
        places = [place.to_dict() for place in city.places]
        return jsonify(places), 200
    return abort(404)


@app_views.route('/places/<id>', strict_slashes=False, methods=['GET'])
def get_place(id):
    """ Method for the "/places/<id>" path GET
    Returns Place by id
    ---
    tags:
      - Place
    parameters:
      - name: id
        in: path
        type: string
        required: true
        description: The ID of State, try 279b355e-ff9a-4b85-8114-6db7ad2a4cd2
    responses:
      200:
        description: A Place object
        examples:
          {
            "__class__":"Place",
            "city_id":"1da255c0-f023-4779-8134-2b1b40f87683",
            "created_at":"2017-03-25T02:17:06.000000",
            "description":"The guest house is located uptown two blocks from Tulane U. The house is located in a very safe and convenient location. The house has a private entrance and patio space. The house also has access to a large backyard with a charcoal grill which is shared. This is a simple, clean and affordable place to stay while visiting New Orleans. We provide everything travelers need. Please contact me if you have any questions.<BR />Thanks,<BR />Ryan<BR /><BR />Note: We have a $50 pet fee",
            "id":"279b355e-ff9a-4b85-8114-6db7ad2a4cd2",
            "latitude":29.9493,
            "longitude":-90.1171,
            "max_guest":2,
            "name":"Guest House by Tulane",
            "number_bathrooms":1,
            "number_rooms":0,
            "price_by_night":60,
            "updated_at":"2017-03-25T02:17:06.000000",
            "user_id":"8394fd35-8a8a-479f-a398-48f53b4a6554"
          }
      404:
        description: When id not found
    """
    place = storage.get(Place, id)
    if place:
        place = place.to_dict()
        return jsonify(place), 200
    return abort(404)


@app_views.route('/places/<id>', strict_slashes=False, methods=['DELETE'])
def delete_place(id):
    """Removes place by id"""
    place = storage.get(Place, id)
    if place:
        storage.delete(place)
        storage.save()
        return jsonify({}), 200
    return abort(404)


@app_views.route('/cities/<id>/places', strict_slashes=False, methods=['POST'])
def create_place(id):
    """Creates a new place"""
    city_exist = storage.get(City, id)
    if city_exist is None:
        return abort(404)
    body = request.get_json(silent=True)
    if body is None:
        return jsonify({'error': 'Not a JSON'}), 400
    if 'user_id' not in body:
        return jsonify({'error': 'Missing user_id'}), 400
    user_exist = storage.get(User, body['user_id'])
    if user_exist is None:
        return abort(404)
    if 'name' not in body:
        return jsonify({'error': 'Missing name'}), 400
    new_place = Place(**body)
    setattr(new_place, 'city_id', id)
    storage.new(new_place)
    storage.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<id>', strict_slashes=False, methods=['PUT'])
def update_place(id):
    """Updates a place"""
    place = storage.get(Place, id)
    if place:
        body = request.get_json(silent=True)
        if body is None:
            return jsonify({'error': 'Not a JSON'}), 400
        if 'user_id' in body:
            user_exist = storage.get(User, body['user_id'])
            if user_exist is None:
                return abort(404)
        for key in body:
            if key != 'id' and key != 'created_at' and key != 'updated_at'\
                    and key != 'user_id' and key != 'city_id':
                setattr(place, key, body[key])
        place.save()
        return jsonify(place.to_dict()), 200
    return abort(404)


================================================


@app_views.route('/amenities/<id>', strict_slashes=False, methods=['GET'])
def get_amenity(id):
    """ Method for the "/amenities/<id>" path GET
    Returns amenity by id
    ---
    tags:
      - Amenity
    parameters:
      - name: id
        in: path
        type: string
        required: true
        description: The ID of State, try 4a0a3fa7-21a0-411a-bb0a-9b4eed1901ef
    responses:
      200:
        description: An Amenity object
        examples:
          {
            "__class__":"Amenity",
            "created_at":"2017-03-25T02:17:06.000000",
            "id":"4a0a3fa7-21a0-411a-bb0a-9b4eed1901ef",
            "name":"Pets allowed",
            "updated_at":"2017-03-25T02:17:06.000000"
          }
      404:
        description: Object not found
    """
    amenity = storage.get(Amenity, id)
    if amenity:
        amenity = amenity.to_dict()
        return jsonify(amenity), 200
    return abort(404)


@app_views.route('/amenities/<id>', strict_slashes=False, methods=['DELETE'])
def delete_amenity(id):
    """Removes amenity by id"""
    amenity = storage.get(Amenity, id)
    if amenity:
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200
    return abort(404)


@app_views.route('/amenities', strict_slashes=False, methods=['POST'])
def create_amenity():
    """Creates a new amenity"""
    body = request.get_json(silent=True)
    if body is None:
        return jsonify({'error': 'Not a JSON'}), 400
    if 'name' in body:
        new_amenity = Amenity(**body)
        storage.new(new_amenity)
        storage.save()
        return jsonify(new_amenity.to_dict()), 201
    else:
        return jsonify({'error': 'Missing name'}), 400


@app_views.route('/amenities/<id>', strict_slashes=False, methods=['PUT'])
def update_amenity(id):
    """Updates an amenity"""
    amenity = storage.get(Amenity, id)
    if amenity:
        body = request.get_json(silent=True)
        if body is None:
            return jsonify({'error': 'Not a JSON'}), 400
        for key in body:
            if key != 'id' and key != 'created_at' and key != 'updated_at':
                setattr(amenity, key, body[key])
        amenity.save()
        return jsonify(amenity.to_dict()), 200
    return abort(404)
