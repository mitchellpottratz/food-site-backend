import os
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from playhouse.shortcuts import model_to_dict
from peewee import DoesNotExist
from exceptions.resource_access_denied import ResourceAccessDenied

from models.food_item import FoodItem 
from models.cart import Cart

import requests
import json

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


# Show Route
# this route is where a user can view a single food item in their cart
@food_items.route('/<food_item_id>', methods=['GET'])
@login_required
def show_food_item(food_item_id):
    try:
        food_item = FoodItem.get(FoodItem.id == food_item_id)
        
        food_item_dict = model_to_dict(food_item)
        del food_item_dict['cart']['user']['password']

        return jsonify(
            data=food_item_dict,
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
                'message': 'Resource does not exist.'
            }
        )



# Create Route
# this route create a new food item from a food item from a restaurant and adds
# it to the users cart
@food_items.route('/', methods=['POST'])
@login_required
def create_food_item():
    data = request.get_json()

    # tries to get the users cart, exception thrown if users cart doesnt exist
    try:
        cart = Cart.get(user=current_user.id)
    except DoesNotExist:
        return jsonify(
            data={},
            status={
                'code': 404,
                'message': 'Resource does not exist.'
            }
        )

    # adds the users cart to the dictionary because FoodItem needs a cart id to be created
    data['cart'] = cart.id

    food_item = FoodItem.create(**data)    
    food_item_dict = model_to_dict(food_item)

    return jsonify(
        data=food_item_dict,
        status={
            'code': 201,
            'message': 'Successfully created resource.'
        }
    )


# search food items route
@food_items.route('/search', methods=["POST"])
# the user does not have to be logged in to search for products
def find_products():
	# get the data from the client
	data = request.get_json()
	# query all the products by the search string
	results = FoodItem.select().where(FoodItem.name.contains(data['name']))
	# iterate over all the searches -- convert to dictionaries
	results_list = []
	for result in results:
		result_dict = model_to_dict(result, backrefs=True, recurse=True)
		results_list.append(result_dict)

	# return success
	return jsonify(data=results_list, status={"code": 200, "message": "Successfully got the search results"})



    





