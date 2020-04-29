#!/usr/bin/python3
"""
Route 
"""

from api.v1.views import app_views, State
from flask import jsonify
from models import storage


@app_views.route('/states', strict_slashes=False, methods=['GET'])
def all_states():
    """Return all states"""
    states = storage.all(State)
    states = [state.to_dict() for state in states.values()]
    return jsonify(states), 200
