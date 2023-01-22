#!/usr/bin/python3
"""register user in blueprint"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """
    Retrieves the list of all User objects
    """
    users = storage.all(User)
    users_list = []
    for user in users.values():
        users_list.append(user.to_dict())
    return jsonify(users_list)


@app_views.route('/users/<user_id>', methods=['GET'],
                 strict_slashes=False)
def get_user(user_id=None):
    """
    Retrieves a User object with the id linked to it
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    else:
        return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def users_delete(user_id=None):
    """delete user by id"""
    user = storage.get('User', user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users/', methods=['POST'], strict_slashes=False)
def users_post():
    """add new user"""
    response = request.get_json()
    if response is None:
        abort(400, description='Not a JSON')
    if 'email' not in response.keys():
        abort(400, description='Missing email')
    if 'password' not in response.keys():
        abort(400, description='Missing password')
    new_user = User(**response)
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def users_put(user_id=None):
    """update user obj"""
    user = storage.get('User', user_id)
    if user is None:
        abort(404)
    response = request.get_json()
    if response is None:
        abort(400, description='Not a JSON')
    response.pop('id', None)
    response.pop('email', None)
    response.pop('created_at', None)
    response.pop('updated_at', None)
    for key, value in response.items():
        setattr(user, key, value)
    storage.save()
    return jsonify(user.to_dict()), 200
