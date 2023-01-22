#!/usr/bin/python3
"""
Flask App start web apication that integrates with AirBnB static HTML
"""

from api.v1.views import app_views
from models import storage
from flask import Flask, make_response, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)

cors = CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})
# Blueprint app_views register
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(exception):
    """
    Metod that after each request call .close() on
    the current session
    """
    storage.close()


@app.errorhandler(404)
def not_found(self):
    """Handlerror 404 - Not found"""
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == "__main__":
    """Main flask app"""
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = os.getenv('HBNB_API_PORT', '5000')
    # Start flask app
    app.run(host=host, port=port, debug=True, threaded=True)
