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


# Create Route 
# this route is where users can create a favorite food
# test restaurant key: a087f8effa313165884225aec137a02a2790e5584fd8fa58
# test food items: 6884330, 6884403, 6884468
@favorite_foods.route('/', methods=['POST'])
@login_required
def create_favorite_food():
    data = request.get_json()
    data['user'] = current_user.id 

    new_favorite_food = FavoriteFood.create(**data)
    new_favorite_food_dict = model_to_dict(new_favorite_food)

    return jsonify(
        data=new_favorite_food_dict,
        status={
            'code': 201,
            'message': 'Resource successfully created.'
        }
    )

   








