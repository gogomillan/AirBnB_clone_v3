#!/usr/bin/python3
"""
Route
"""

from api.v1.views import app_views, State
from flask import jsonify, abort
from models import storage


@app_views.route('/states', strict_slashes=False, methods=['GET'])
def all_states():
    """Return all states"""
    states = storage.all(State)
    states = [state.to_dict() for state in states.values()]
    return jsonify(states), 200


@app_views.route('/states/<id>', strict_slashes=False, methods=['GET'])
def get_state(id):
    """Return state by id"""
    state = storage.get(State, id)
    if state:
        state = state.to_dict()
        return jsonify(state), 200
    return abort(404)
