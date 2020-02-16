import os
from flask import request, jsonify, Blueprint
from peewee import DoesNotExist

# blueprint for Restaurant
restaurants = Blueprint('user', 'user')

# how to obtain keys out of .env file
all_restaurants = os.environ['API_KEY']

# route to list all restaurants from api
@restaurants.route('/allRestaurants', methods=["GET"])
def list_restaurants():
    data = requests.get('https://eatstreet.com/' + all_restaurants + '/v1/restaurant/search?method=both&pickup-radius=100&street-address=520+W+Taylor+St.,+Chicago,+IL')
    return data.text

    