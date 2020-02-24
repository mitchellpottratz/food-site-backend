from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from playhouse.shortcuts import model_to_dict
from peewee import DoesNotExist
from exceptions.resource_access_denied import ResourceAccessDenied

from models.food_item_customization import FoodItemCustomization
from models.food_item import FoodItem


food_item_customizations = Blueprint('food_item_customizations', 'food_item_customizations')


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

    # now the food item customization gets createds
    customization = FoodItemCustomization.create(
        food_item=data['food_item_id'], api_key=data['apiKey'],
        name=data['name'], price=data['price'], count=data['count']
    )
    customization_dict = model_to_dict(customization)

    return jsonify(
        data=customization_dict,
        status={
            'code': 201,
            'message': 'Successfully created resource.'
        }
    )


    



