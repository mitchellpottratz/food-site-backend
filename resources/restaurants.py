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

# index route -- list all restaurants from api (base will be from Taylor St in Chicago)
@restaurants.route('/', methods=["GET"])
def list_restaurants():
    response = requests.get("https://eatstreet.com/publicapi/v1/restaurant/search?method=both&pickup-radius=100&street-address=223+S+Wacker+Dr.,Chicago,+IL", headers={'X-Access-Token': os.environ['API_KEY']})
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
    # gets the query params used for searching for restaurants
    street_address = request.args.get('street_address')
    pickup_radius = request.args.get('pickup_radius')
    search_term = request.args.get('search_term')

    # creates the request headers and formats the api url with the correct query parameters
    api_request_headers = {'X-Access-Token': os.environ['API_KEY']}
    formatted_api_url = (api_url + '&street-address=' + street_address +
                                   '&pickup-radius=' + pickup_radius + 
                                   '&search=' + search_term)

    # makes a request to the api and parses the response
    api_response = requests.get(formatted_api_url, headers=api_request_headers)
    parsed_api_response = api_response.json()

    # tries to return the restaurants if their were any found
    try: 
        return jsonify(
            data=parsed_api_response['restaurants'],
            status={
                'code': 200,
                'message': 'Successfully found restaurants.'
            }
        ) 
    # if their are no restaurants found
    except KeyError:
        return jsonify(
            data={},
            status={
                'code': 200,
                'message': 'No restaurants found. Try to increase your pickup radius.'
            }
        )

# show route
@restaurants.route('/<restaurant_api_key>', methods=['GET'])
def get_single_restaurant(restaurant_api_key):
    # make api call
    response = requests.get('https://eatstreet.com/publicapi/v1/restaurant/' + restaurant_api_key, headers={'X-Access-Token': os.environ['API_KEY']})
    try:
        data = response.json()
        return jsonify(data=data, status={"code": 200, "message": "successfully loaded single restaurants"}), 200
    except:
        # return error message if data cannot be processed 
        return jsonify(data={}, status={'code': 500,'message': 'error loading your restaurant'}), 500

