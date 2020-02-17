import os
from flask import request, jsonify, Blueprint
from peewee import DoesNotExist
from playhouse.shortcuts import model_to_dict

# handles requests from 3rd party api
import requests
import json

# blueprint for Restaurant
restaurants = Blueprint('restaurants', 'restaurants')

# EatStreet api url
api_url = 'https://eatstreet.com/publicapi/v1/restaurant/search?method=both'

# how to obtain keys out of .env file (API_KEY)
all_restaurants_token = os.environ['API_KEY']

# route to list all restaurants from api
@restaurants.route('/', methods=["GET"])
def list_restaurants():
    response = requests.get("https://eatstreet.com/publicapi/v1/restaurant/search?method=both&pickup-radius=100&street-address=520+W+Taylor+St.,+Chicago,+IL", headers={'X-Access-Token': all_restaurants_token})
    try:
        data = response.json()
        return jsonify(data=data['restaurants'], status={"code": 200, "message": "successfully loaded all restaurants"}), 200
    except:
        # return error message if data cannot be processed 
        return jsonify(data={}, status={'code': 500,'message': 'error loading all restaurants'}), 500


# Search Route
# makes an api call to find restuarants near the users current location
@restaurants.route('/search', methods=['GET'])
def search_restaurants():
    try:
        data = request.get_json()

        # for filtering the results
        search_term = data['search_term']

        # the users location
        longitude = data['longitude']
        latitude = data['latitude']

    # throws exception if any fields in the request body are missing
    except KeyError:
        return jsonify(
            data={},
            status={
                'code': 422,
                'status': 'Invalid request body.'
            }
        )

    
    




