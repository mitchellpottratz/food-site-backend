from flask import Blueprint, request, jsonify
from playhouse.shortcuts import model_to_dict

# model imports 
from models.address import Address 
from models.user import User

addresses = Blueprint('addresses', 'addresses')


# Ping Route
@addresses.route('/ping', methods=['GET'])
def ping():
    return jsonify(
		data={},
		status={
			'code': 200,
			'message': 'Resource is working.'
		}
	)