import os
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from playhouse.shortcuts import model_to_dict
from peewee import DoesNotExist
from exceptions.resource_access_denied import ResourceAccessDenied

from models.food_item_customization import FoodItemCustomization
from models.food_item import FoodItem

import requests

food_item_customizations = Blueprint('food_item_customizations', 'food_item_customizations')

# EatStreet food item customizations api url
customizations_api_url = 'https://eatstreet.com/publicapi/v1/customizations/'


# Ping Route
@food_item_customizations.route('/ping', methods=['GET'])
def ping():
    return jsonify(
        data={},
        status={
            'code': 200,
            'message': 'Resource is working.'
        }
    )


# Show Route
# this route is where a user can view all of the customizations options for a food item
@food_item_customizations.route('/<food_item_api_key>', methods=['GET'])
@login_required
def show_customization_options(food_item_api_key):

    # makes api call to get all customizable options for a food item
    response = requests.get(
        customizations_api_url + food_item_api_key,
        headers={'X-Access-Token': os.environ['API_KEY']}
    )
    customization_options = response.json()


    return jsonify(
        data=customization_options,
        status={
            'code': 200,
            'message': 'Successfully got resource.'
        }
    )


# Create Route
# this route is where a user can add a food item customization to a food item
@food_item_customizations.route('/', methods=['POST'])
@login_required
def create_customization():
    data = request.get_json()

    # checks if the food item being customized exists
    try:
        food_item = FoodItem.get(FoodItem.id == data['food_item_id'])
    except DoesNotExist:
        return jsonify(
            data={},
            status={
                'code': 404,
                'message': 'Resource does not exist'
            }
        )

    # now the food item customization gets created
    customization = FoodItemCustomization.create(
        food_item=data['food_item_id'], 
        selection_api_key=data['selection_api_key'],
        choice_api_key=data['choice_api_key'],
        selection_name=data['selection_name'],
        choice_name=data['choice_name'],
        price=data['price'],
        count=data['count']
    )
    customization_dict = model_to_dict(customization)

    return jsonify(
        data=customization_dict,
        status={
            'code': 201,
            'message': 'Successfully created resource.'
        }
    )


    



