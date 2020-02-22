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


# Index Route
# this route returns all of the users favorite foods
@favorite_foods.route('/', methods=['GET'])
@login_required
def get_all_favorite_foods():
    all_favorite_foods = FavoriteFood.select().where(FavoriteFood.user == current_user.id)

    # converts all of the favorite foods model instances to dictionaries
    all_favorite_foods_dict = [model_to_dict(favorite_food) for favorite_food in all_favorite_foods]

    return jsonify(
        data=all_favorite_foods_dict,
        status={
            'code': 200,
            'message': 'Successfully found resources.'
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

    # checks if the favorite food item the user is creating already exists
    try:
        existing_favorite_food = FavoriteFood.get(
            FavoriteFood.user == current_user.id,
            FavoriteFood.food_item_api_key == data['food_item_api_key']
        )

        return jsonify(
            data={},
            status={
                'code': 403,
                'message': 'Resource already exists.'
            }
        )
    
    # if the favorite food item doesnt already exist then a new one is created
    except DoesNotExist:
        new_favorite_food = FavoriteFood.create(**data)

        new_favorite_food_dict = model_to_dict(new_favorite_food)
        del new_favorite_food_dict['user']['password']

        return jsonify(
            data=new_favorite_food_dict,
            status={
                'code': 201,
                'message': 'Resource successfully created.'
            }
        )


# Delete Route
# this route is where users can delete one of their food items
@favorite_foods.route('/<food_id>', methods=['DELETE'])
@login_required
def delete_favorite_food(food_id):
    try:
        favorite_food_to_delete = FavoriteFood.get(FavoriteFood.id == food_id)
        favorite_food_to_delete.delete_instance()

        return jsonify(
            data={},
            status={
                'code': 204,
                'message': 'Successfully deleted resource.'
            }
        )

    except DoesNotExist:
        return jsonify(
            data={},
            status={
                'code': 404,
                'message': 'Resources does not exist.'
            }
        )
   








