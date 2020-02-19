from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from playhouse.shortcuts import model_to_dict
from peewee import DoesNotExist
from exceptions.resource_access_denied import ResourceAccessDenied

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


# Show Route
# this route shows a single users cart 
@carts.route('/<cart_id>', methods=['GET'])
@login_required
def show_users_cart(cart_id):
    try:
        cart = Cart.get(id=cart_id)

        # throws an exception if the user is not the user of the cart
        try:
            if not cart.user_is_owner(current_user.id):
                raise ResourceAccessDenied()
        except ResourceAccessDenied as e:
            return e.get_json_response()

        cart_dict = model_to_dict(cart)
        del cart_dict['user']['password']

        return jsonify(
            data=cart_dict,
            status={
                'code': 200,
                'message': 'Successfully found resource.'
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


# Delete Route
# this route is where a users cart can be deleted
@carts.route('/<cart_id>', methods=['DELETE'])
@login_required
def delete_users_cart(cart_id):
    try:
        cart = Cart.get(id=cart_id)

        # throws an exception if the user is not the user of the queried cart
        try:
            if not cart.user_is_owner(current_user.id):
                raise ResourceAccessDenied()
        except ResourceAccessDenied as e:
            return e.get_json_response()

        # deletes the cart the user is verified as the carts user
        cart.delete_instance()  

        return jsonify(
            data={},
            status={
                'code': 204,
                'message': 'Resource deleted successfully.'
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


      




