# import models here
from models.user import User

from flask import request, jsonify, Blueprint, session
from peewee import DoesNotExist

# password and logging in
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, current_user, logout_user, login_required

# convert models to dictionaries
from playhouse.shortcuts import model_to_dict

# blueprint for User
users = Blueprint('user', 'user')


# Ping Route
# for testing purposes
@users.route('/', methods=['GET'])
def ping():
	return jsonify(
		data={},
		status={
			'code': 200,
			'message': 'Resource is working.'
		}
	)


# Show Route
# returns a single user queried by their id
@users.route('/<user_id>', methods=['GET'])
def get_user(user_id):
	try:
		user = User.get(User.id == user_id)
		user_dict = model_to_dict(user)
		del user_dict['password']

		return jsonify(
			data=user_dict,
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
		), 201


# Login Route
@users.route('/login', methods=['POST'])
def login():
	data = request.get_json()
	try:
		user = User.get(User.email == data['email'])

		# if the password is correct
		if check_password_hash(user.password, data['password']):
			login_user(user)

			user_dict = model_to_dict(user)
			del user_dict['password']

			return jsonify(
				data=user_dict,
				status={
					'code': 200,
					'message': 'Successfully logged in'
				}
			)
		# if the password is incorrect
		else:
			return jsonify(
				data={},
				status={
					'code': 404,
					'message': 'Email or password is incorrect.'
				}
			)
	# if the provided email does not match any users
	except DoesNotExist:
		return jsonify(
			data={},
			status={
				'code': 404,
				'message': 'Email or password is incorrect.'
			}
		)

# # post route (favorite a food)
# @users.route('/favorite_this_food/<food_item_apiKey>', methods=['POST'])
# def favorite_a_food(food_item_apiKey):
# 	# data = request.get_json()
# 	# print("data:", data)
# 	# find the user that is logged in
# 	try:
# 		# first the get the user
# 		user = User.get(User.email == data['email'])
# 		# create the favorite food item and add this to the user
# 		favorite_food = models.User.create(food_item_apiKey=food_item_apiKey)
# 		# convert to dictionary
# 		favorite_food_dict = model_to_dict(favorite_food)
# 		return jsonify(data=favorite_food_dict, status={'code': 201, 'message': 'successfully added food item to your favorite food collection'})
# 	except:
# 		return jsonify(data={}, status={'code': 500,'message': 'error adding your food to your favorite collection'}), 500

# log out route
@users.route('/logout', methods=["GET"])
def logout():
    # get the email of the user
    email = model_to_dict(current_user)['email']
    # log out the user
    logout_user()
    # return success
    return jsonify(data={}, status={"code": 200, "message": "Successfully logged out {}".format(email)})

