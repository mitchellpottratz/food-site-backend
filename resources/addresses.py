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
@addresses.route('/', methods=['POST'])
@login_required
def create_address():
    pass

