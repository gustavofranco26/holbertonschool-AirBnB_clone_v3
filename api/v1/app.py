#!/usr/bin/python3
"""
Flask App start web apication that integrates with AirBnB static HTML
"""

from api.v1.views import app_views
from models import storage
from flask import Flask
import os

app = Flask(__name__)


# Blueprint app_views register
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(exception):
    """
    Metod that after each request call .close() on
    the current session
    """
    storage.close()

if __name__ == "__main__":
    """
    Main flask App 
    """
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = os.getenv('HBNB_API_PORT', '5000')
    app.run(host=host, port=port, debug=True, threaded=True) #Start flask app
