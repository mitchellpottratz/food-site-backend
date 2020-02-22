from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from playhouse.shortcuts import model_to_dict
from peewee import DoesNotExist
from exceptions.resource_access_denied import ResourceAccessDenied

# model imports 
from models.address import Address 
from models.user import User

addresses = Blueprint('addresses', 'addresses')


# Ping Route
@addresses.route('/ping', methods=['GET'])
@login_required
def ping():
    return jsonify(
		data={},
		status={
			'code': 200,
			'message': 'Resource is working.'
		}
	)


# Index Route
# this route returns all of the addresses that exist for the current user
@addresses.route('/', methods=['GET'])
@login_required
def get_users_addresses():
    try:
        all_addresses = Address.select().where(Address.user == current_user.id)

        # converts the address model instances to dictionaries
        all_addresses_dict = [model_to_dict(address) for address in all_addresses]

        # iterates through all the model instances and converts them to a dictionary and removes 
        # the users password
        all_addresses_dict = []
        for address in all_addresses:
            address_dict = model_to_dict(address)
            del address_dict['user']['password']
            all_addresses_dict.append(address_dict)


        return jsonify(
            data=all_addresses_dict,
            status={
                'code': 200,
                'message': 'Successfully found resources.'
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
# this route is where users can create a new delivery address
@addresses.route('/', methods=['POST'])
@login_required
def create_address():
    data = request.get_json()

    # attach the users id to the dictionary to specify which user is creating the address
    data['user'] = current_user.id 

    new_address = Address.create(**data)
    new_address_dict = model_to_dict(new_address)

    # so the users password hash isnt return in the response
    del new_address_dict['user']['password']

    return jsonify(
        data=new_address_dict,
        status={
            'code': 201,
            'message': 'New resource created.'
        }
    )


# Show Route
# this route is where the user can get one of their addresses
@addresses.route('/<address_id>', methods=['GET'])
@login_required
def show_users_address(address_id):
    try:
        address = Address.get(Address.id == address_id)

        # throws a access denied error if the user is not the owner of the address instance
        try:
            if not address.user_is_owner(current_user.id):
                raise ResourceAccessDenied()
        except ResourceAccessDenied as e:
            return e.get_json_response()
        
        address_dict = model_to_dict(address)
        del address_dict['user']['password']

        return jsonify(
            data=address_dict,
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


# Update Route
# updates a users address
@addresses.route('/<address_id>', methods=['PUT'])
@login_required
def update_address(address_id):
    data = request.get_json()

    try:
        address = Address.get(Address.id == address_id)

        # checks if the user is the creator of the address, if not an exception is thrown
        try:
            if not address.user_is_owner(current_user.id):
                raise ResourceAccessDenied()
        except ResourceAccessDenied as e:
            return e.get_json_response()

        # updates the address
        address.name = data['name']
        address.address = data['address']
        address.instructions = data['instructions']
        address.save()

        updated_address_dict = model_to_dict(address)

        return jsonify(
            data=updated_address_dict,
            status={
                'code': 204,
                'message': 'Successfully updated the resource'
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


# Delete Route
# deletes a users address
@addresses.route('/<address_id>', methods=['DELETE'])
@login_required
def delete_address(address_id):
    try: 
        address_to_delete = Address.get(Address.id == address_id)

        # checks if the user is the creator of the address, if not an exception is thrown
        try:
            if not address_to_delete.user_is_owner(current_user.id):
                raise ResourceAccessDenied()
        except ResourceAccessDenied as e:
            return e.get_json_response()

        # after the user of the model instance is verified then its deleted
        address_to_delete.delete_instance()

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
                'message': 'Resource does not exist'
            }
        )












