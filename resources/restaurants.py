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
        street_address = request.args.get('street_address')
        pickup_radius = request.args.get('pickup_radius')
        search_term = request.args.get('search_term')

    except KeyError:
        return jsonify(
            data={},
            status={
                'code': 422,
                'status': 'Invalid query parameters'
            }
        )

    # creates the request headers and formats the api url with the correct query parameters
    api_request_headers = {'X-Access-Token': os.environ['API_KEY']}
    formatted_api_url = (api_url + '&street-address=' + street_address +
                                   '&pickup-radius=' + pickup_radius + 
                                   '&search=' + search_term)

    # makes a request to the api and parses the response
    api_response = requests.get(formatted_api_url, headers=api_request_headers)
    parsed_api_response = api_response.json()

    return jsonify(
        data=parsed_api_response['restaurants'],
        status={
            'code': 200,
            'message': 'Successfully found restaurants.'
        }
    )


    
    




