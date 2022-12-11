#!/usr/bin/python3
"""
Flask index file that returns the json status response
"""


from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route('/status')
def status():
    """Function for status route, return status"""
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def stats():
    """Method stats"""
    return jsonify(
            {
                "amenities": storage.count("Amenity"),
                "cities": storage.count("City"),
                "places": storage.count("Place"),
                "reviews": storage.count("Review"),
                "states": storage.count("State"),
                "users": storage.count("User"),
                })
