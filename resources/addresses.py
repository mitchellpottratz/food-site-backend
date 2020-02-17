from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from playhouse.shortcuts import model_to_dict

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

    return jsonify(
        data=new_address_dict,
        status={
            'code': 201,
            'message': 'New delivery address created'
        }
    )



