#!/usr/bin/python3
"""
Route
"""

from api.v1.views import app_views, State
from flask import jsonify, abort
from models import storage


@app_views.route('/states', strict_slashes=False, methods=['GET'])
def all_states():
    """Returns all states"""
    states = storage.all(State)
    states = [state.to_dict() for state in states.values()]
    return jsonify(states), 200


@app_views.route('/states/<id>', strict_slashes=False, methods=['GET'])
def get_state(id):
    """Returns state by id"""
    state = storage.get(State, id)
    if state:
        state = state.to_dict()
        return jsonify(state), 200
    return abort(404)


@app_views.route('/states/<id>', strict_slashes=False, methods=['DELETE'])
def delete_state(id):
    """Removes state by id"""
    state = storage.get(State, id)
    if state:
        storage.delete(state)
        storage.save()
        return jsonify({}), 200
    return abort(404)
