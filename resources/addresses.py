from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from playhouse.shortcuts import model_to_dict
from peewee import DoesNotExist

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
def get_users_addresses():
    try:
        all_addresses = Address.select().where(Address.user == current_user.id)

        # converts the queried addresses to a dictionary
        all_addresses_dict = [model_to_dict(address) for address in all_addresses]

        return jsonify(
            data=all_addresses_dict,
            status={
                'code': 200,
                'message': 'Successfully got resources'
            }    
        )

    except DoesNotExist:
        return jsonify(
            data={},
            status={
                'code': 200,
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



