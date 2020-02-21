from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from playhouse.shortcuts import model_to_dict

from peewee import DoesNotExist
from exceptions.resource_access_denied import ResourceAccessDenied

from models.favorite_food import FavoriteFood
from models.user import User


favorite_foods = Blueprint('favorite_foods', 'favorite_foods')


# Ping Route
@favorite_foods.route('/ping', methods=['GET'])
def ping():
    return jsonify(
        data={},
        status={
            'code': 200,
            'message': 'Resource is working.'
        }
    )




