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


# Create Route
# this route create a new food item from a food item from a restaurant and adds
# it to the users cart
@food_items.route('/', methods=['POST'])
@login_required
def create_food_item():
    data = request.get_json()

    try: 
        


    





