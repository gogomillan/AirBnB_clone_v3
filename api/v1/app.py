#!/usr/bin/python3
"""
Flask API v1
"""

from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)

app.register_blueprint(app_views)

host = getenv('HBNB_API_HOST') or 5000
port = getenv('HBNB_API_PORT') or '0.0.0.0'


@app.teardown_appcontext
def teardown(self):
    """Calls close session storage"""
    storage.close()

if __name__ == "__main__":
    app.run(host=host, port=port, threaded=True)
