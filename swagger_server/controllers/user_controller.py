import connexion
import six

from models.user import User
from models.user_token import UserToken
from models.user_update import UserUpdate
import util
from flask import jsonify
from flask_cors import cross_origin
from easy_jwt import auth
from __main__ import worker


def create_user(userdata):
    if connexion.request.is_json:
        userdata_read = User.from_dict(connexion.request.get_json())

        try:
            worker.control_tool.register_guy(userdata_read)
        except:
            return "Bad data", 400
    else:
        return "Bad data", 400

    return "Success", 200


def delete_user(username):
    authorization = connexion.request.headers['Authorization']

    if auth.verify_token(authorization):
        try:
            worker.control_tool.delete_guy(username)
        except:
            return "User is not found", 404
    else:
        return "Unauthorized", 401

    return 'Success', 200


def get_unique_user(username):
    authorization = connexion.request.headers['Authorization']

    if auth.verify_token(authorization):
        try:
            user = worker.control_tool.get_guy_user(username)
        except:
            return "User is not found", 404
    else:
        return "Unauthorized", 401

    return jsonify(username=user['username'], lastName=user['lastName'], firstName=user['firstName'], password=user['password'], gender=user['gender']), 200


def login(username, password):
    check = worker.control_tool.login_guy(username, password)
    if check == 200:
        token = auth.create_token(username)
        return jsonify(token=token), 200

    elif check == 400:
        return "Invalid login/password", 400

    else:
        return "Server error", 500


def logout():
    authorization = connexion.request.headers['Authorization']
    """Logs out current logged in user session

     # noqa: E501

    :param authorization: 
    :type authorization: str

    :rtype: None
    """
    return 'None', 501


def patch_user_data(username, body):
    authorization = connexion.request.headers['Authorization']

    if auth.verify_token(authorization):
        try:
            worker.control_tool.update_data(username, body)
        except:
            return "Bad data", 400
    else:
        return "Bad data", 400

    return "Success", 200
