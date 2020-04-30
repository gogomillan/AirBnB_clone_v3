#!/usr/bin/python3
"""
Script for the cities API RESTful API
"""
from api.v1.views import app_views, State, City
from flask import jsonify, abort, request
from models import storage


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['GET'])
def get_cities_state(id):
    """Returns state by id"""
    state = storage.get(State, id)
    if state:
        cities = [state.to_dict() for state in states.cities]
        return jsonify(cities), 200
    return abort(404)


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['GET'])
def get_city(id):
    """Returns state by id"""
    city = storage.get(City, id)
    if city:
        city = city.to_dict()
        return jsonify(city), 200
    return abort(404)


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['DELETE'])
def delete_city(id):
    """Removes state by id"""
    city = storage.get(City, id)
    if city:
        storage.delete(city)
        storage.save()
        return jsonify({}), 200
    return abort(404)


@app_views.route('/states/<state_id>/cities', strict_slashes=False, methods=['POST'])
def create_state(state_id):
    """Creates a new state"""
    state = storage.get(State, id)
    if not bool(state):
        return abort(404)

    body = request.get_json(silent=True)
    if body is None:
        return jsonify({'error': 'Not a JSON'}), 400

    if 'name' in body:
        new_city = City(**body)
        new_city.state_id = state.id
        storage.new(new_city)
        storage.save()
        return jsonify(new_city.to_dict()), 201
    else:
        return jsonify({'error': 'Missing name'}), 400


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['PUT'])
def update_city(id):
    """Updates a state"""
    city = storage.get(City, id)
    if city:
        body = request.get_json(silent=True)
        if body is None:
            return jsonify({'error': 'Not a JSON'}), 400
        for key in body:
            print(city.__class__.name)
            if key != 'id' and key != 'created_at' and key != 'updated_at':
                setattr(city, key, body[key])
        city.save()
        return jsonify(city.to_dict()), 200
    return abort(404)
