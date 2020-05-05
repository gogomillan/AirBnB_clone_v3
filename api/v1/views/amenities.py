#!/usr/bin/python3
"""
Route
"""

from api.v1.views import app_views, Amenity
from flask import jsonify, abort, request
from models import storage


@app_views.route('/amenities', strict_slashes=False, methods=['GET'])
def all_amenities():
    """ Method for the "/amenities" path GET
    Returns all amenities
    ---
    tags:
      - Amenity
    responses:
      200:
        description: A list of all Amenity objects
        examples:
          [
            {
              "__class__":"Amenity",
              "created_at":"2017-03-25T02:17:06.000000",
              "id":"4a0a3fa7-21a0-411a-bb0a-9b4eed1901ef",
              "name":"Pets allowed",
              "updated_at":"2017-03-25T02:17:06.000000"
            },
            {
              "__class__":"Amenity",
              "created_at":"2017-03-25T02:17:06.000000",
              "id":"6b9c3987-a344-4baf-8d11-077d719688ba",
              "name":"Lock on bedroom door",
              "updated_at":"2017-03-25T02:17:06.000000"
            }
          ]
    """
    amenities = storage.all(Amenity)
    amenities = [amenity.to_dict() for amenity in amenities.values()]
    return jsonify(amenities), 200


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
        description: A State object
        examples:
          {
            "__class__":"Amenity",
            "created_at":"2017-03-25T02:17:06.000000",
            "id":"4a0a3fa7-21a0-411a-bb0a-9b4eed1901ef",
            "name":"Pets allowed",
            "updated_at":"2017-03-25T02:17:06.000000"
          },
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


====================================================


@app_views.route('/states/<id>', strict_slashes=False, methods=['GET'])
def get_state(id):
    """ Method for the "/states/<id>" path GET
    Returns state by id
    ---
    tags:
      -   State
    parameters:
      - name: id
        in: path
        type: string
        required: true
        description: The ID of State, try 5976f0e7-5c5f-4949-aae0-90d68fd239c0
    responses:
      200:
        description: A State object
        examples:
          {
            "__class__": "State", 
            "created_at": "2017-04-14T00:00:02", 
            "id": "8f165686-c98d-46d9-87d9-d6059ade2d99", 
            "name": "Louisiana", 
            "updated_at": "2017-04-14T00:00:02"
          }
      404:
        description: Object not found
    """
    states = storage.all(State)
    state = storage.get(State, id)
    if state:
        state = state.to_dict()
        return jsonify(state), 200
    return abort(404)


@app_views.route('/states/<id>', strict_slashes=False, methods=['DELETE'])
def delete_state(id):
    """ Method for the "/states/<id>" path DELETE
    Removes state by id
    ---
    tags:
      -   State
    parameters:
      - name: id
        in: path
        type: string
        required: true
        description: The ID of State, create one and try its ID
    responses:
      200:
        description: Object deleted
        examples:
            {}
      404:
        description: Object not found
    """
    state = storage.get(State, id)
    if state:
        storage.delete(state)
        storage.save()
        return jsonify({}), 200
    return abort(404)


@app_views.route('/states', strict_slashes=False, methods=['POST'])
def create_state():
    """ Method for the "/states" path POST
    Creates a new state
    ---
    tags:
      -   State
    parameters:
      - in: body
        name: body
        required: true
        content:
          application/json:
        schema:
          properties:
            name:
              type: string
              description: Name for the state
    responses:
      201:
        description: A State object was created
        examples:
          {
            "__class__": "State", 
            "created_at": "2017-04-15T01:30:27.557877", 
            "id": "feadaa73-9e4b-4514-905b-8253f36b46f6", 
            "name": "California", 
            "updated_at": "2017-04-15T01:30:27.558081"
          }
      400:
        description: When error in JSON or in data
        examples:
          {
            "error": "Not a JSON"
          }
        examples:
          {
            "error": "Missing name"
          }
    """
    body = request.get_json(silent=True)
    if body is None:
        return jsonify({'error': 'Not a JSON'}), 400
    if 'name' in body:
        new_state = State(**body)
        storage.new(new_state)
        storage.save()
        return jsonify(new_state.to_dict()), 201
    else:
        return jsonify({'error': 'Missing name'}), 400


@app_views.route('/states/<id>', strict_slashes=False, methods=['PUT'])
def update_state(id):
    """ Method for the "/states/<id>" path PUT
    Updates a state
    ---
    tags:
      -   State
    parameters:
      - in: body
        name: body
        required: true
        content:
          application/json:
        schema:
          properties:
            name:
              type: string
              description: Name for the state
      - in: path
        name: id
        type: string
        required: true
        description: The ID of State, try 5976f0e7-5c5f-4949-aae0-90d68fd239c0
    responses:
      200:
        description: A State object was modified
        examples:
          {
            "__class__": "State",
            "created_at": "2017-04-15T01:30:27.557877",
            "id": "feadaa73-9e4b-4514-905b-8253f36b46f6",
            "name": "California",
            "updated_at": "2017-04-15T01:30:27.558081"
          }
      400:
        description: When error in JSON
        examples:
          {
            "error": "Not a JSON"
          }
      404:
        description: When id not found
    """
    state = storage.get(State, id)
    if state:
        body = request.get_json(silent=True)
        if body is None:
            return jsonify({'error': 'Not a JSON'}), 400
        for key in body:
            if key != 'id' and key != 'created_at' and key != 'updated_at':
                setattr(state, key, body[key])
        state.save()
        return jsonify(state.to_dict()), 200
    return abort(404)
