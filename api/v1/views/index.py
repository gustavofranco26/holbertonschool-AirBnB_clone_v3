#!/usr/bin/python3
"""
Flask index file that returns the json status response
"""


from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status')
def status():
    """Function for status route, return status"""
    return jsonify({"status": "OK"})
