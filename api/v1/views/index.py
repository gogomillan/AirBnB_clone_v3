#!/usr/bin/python3
"""
Route Index
"""

from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', strict_slashes=False, methods=['GET'])
def status():
    return jsonify({'status': 'ok'}), 200
