from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from playhouse.shortcuts import model_to_dict
from peewee import DoesNotExist

from models.cart import Cart 
from models.user import User  

carts = Blueprint('carts', 'carts')


# Ping Route
@carts.route('/ping', methods=['GET'])
def ping():
    return jsonify(
        data={},
        status={
            'code': 200,
            'Resource': 'IM ALIVE!!!!!!'
        }
    )


# Create Route
# this route creates a new cart for a user
@carts.route('/', methods=['POST'])
@login_required
def create_users_cart():
    new_cart = Cart.create(user=current_user.id)

    new_cart_dict = model_to_dict(new_cart)
    del new_cart_dict['user']['password']

    return jsonify(
        data=new_cart_dict,
        status={
            'code': 201,
            'message': 'Successfully created resource.'
        }
    )  

      




