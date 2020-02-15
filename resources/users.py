# import models here
from models.user import User

from flask import request, jsonify, Blueprint
from peewee import DoesNotExist

# password and logging in
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, current_user, logout_user, login_required

# convert models to dictionaries
from playhouse.shortcuts import model_to_dict

# blueprint for User
users = Blueprint('user', 'user')


# just for testing
@users.route('/ping', methods=['GET'])
def ping():
	return jsonify(
		data={},
		status={
			'code': 200,
			'message': 'Users controller is working' 
		}
	)


# registration route
@users.route('/register', methods=['POST'])
def register():
	# this is the payload
	data = request.get_json()
	try:
		# queries a user by the provided email
		User.get(User.email == data['email'])

		# return error
		return jsonify(
			data={},
			status={'code': 401,
					'message': 'A user with that email already exists.',
					'field_error': 'email'}
		)

	# if there is no error, do the following
	except DoesNotExist:
		# encrypts the password
		data['password'] = generate_password_hash(data['password'])
		# create user in database
		user = User.create(**data)
		# logs in user
		login_user(user)
		# convert user to dictionary and remove password
		user_dict = model_to_dict(user, backrefs=True, recurse=True)
		del user_dict['password']
        # return success
		return jsonify(
			data=user_dict,
			status={'code': 201, 'message': 'Successfully registered {}.'.format(user_dict['email'])}
		)


