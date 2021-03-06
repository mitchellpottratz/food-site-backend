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

    # iterates through all the model instances and converts them to a dictionary and removes 
    # the users password
    all_favorite_foods_dict = []
    for favorite_food in all_favorite_foods:
        favorite_food_dict = model_to_dict(favorite_food)
        del favorite_food_dict['user']['password']
        all_favorite_foods_dict.append(favorite_food_dict) 

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


# Show Route
# this route is where user can get one of their favorite food items
@favorite_foods.route('/<food_id>', methods=['GET'])
@login_required
def show_favorite_food(food_id):
    try:
        favorite_food = FavoriteFood.get(FavoriteFood.id == food_id)

        # throws a access denied error if the user is not the owner of this favorite food instance
        try:
            if not favorite_food.user_is_owner(current_user.id):
                raise ResourceAccessDenied()
        except ResourceAccessDenied as e:
            return e.get_json_response()
    
        favorite_food_dict = model_to_dict(favorite_food)
        del favorite_food_dict['user']['password']

        return jsonify(
            data=favorite_food_dict,
            status={
                'code': 200,
                'message': 'Successfully got resource.'
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


# Delete Route
# this route is where users can delete one of their food items
@favorite_foods.route('/<food_id>', methods=['DELETE'])
@login_required
def delete_favorite_food(food_id):
    try:
        favorite_food_to_delete = FavoriteFood.get(FavoriteFood.id == food_id)

        # throws a access denied error if the user is not the owner of this favorite food instance
        try:
            if not favorite_food_to_delete.user_is_owner(current_user.id):
                raise ResourceAccessDenied()
        except ResourceAccessDenied as e:
            return e.get_json_response()

        # now that the current user is verified as the model instance owner it gets deleted
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
   








