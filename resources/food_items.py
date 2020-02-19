from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from playhouse.shortcuts import model_to_dict
from peewee import DoesNotExist
from exceptions.resource_access_denied import ResourceAccessDenied

from models.food_item import FoodItem 
from models.cart import Cart

food_items = Blueprint('food_items', 'food_items')


# Ping Route
@food_items.route('/ping', methods=['GET'])
def ping():
    return jsonify(
        data={},
        status={
            'code': 200,
            'Resource': 'IM ALIVE!!!!!!'
        }
    )


# Create Route - NOT FINISHED
# this route create a new food item from a food item from a restaurant and adds
# it to the users cart
@food_items.route('/', methods=['POST'])
@login_required
def create_food_item():
    data = request.get_json()
    restaurant_api_key = data['restaurant_api_key']
    food_item_api_key = data['food_item_api_key']

    # makes api call to get all the items in the restaurants menu
    menu = FoodItem.get_restaurants_menu(restaurant_api_key)

    # gets the food item from the resturants menu
    food_item = FoodItem.get_food_item(menu, food_item_api_key)

    return jsonify(
        data=menu,
        status={
            'code': 201,
            'message': 'Successfully created resource.'
        }
    )



    





