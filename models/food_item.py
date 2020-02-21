import os
from peewee import *
from .base_food_item import BaseFoodItem
from .cart import Cart
import requests
import json

''' 
This model represents a food item that is in a users cart from the EatStreet api 
'''

class FoodItem(BaseFoodItem):
    cart = ForeignKeyField(Cart, backref='food-items')

    # the api url to search for a restaurants menu
    API_URL = 'https://eatstreet.com/publicapi/v1/restaurant/'

    # header that needs to be sent in the request to the EatStreet api
    API_HEADER = {'X-Access-Token': os.environ['API_KEY']}
   
    # makes a request to the EatStreet api to get all of the food item on a restaurants menu
    @staticmethod
    def get_restaurants_menu(restaurant_api_key):
        response = requests.get(FoodItem.API_URL + restaurant_api_key +
                                '/menu', headers=FoodItem.API_HEADER)
        parsed_response = response.json()
        return parsed_response

    # parses the restaurants menu and returns the matching food item
    @staticmethod
    def get_food_item(menu, food_item_api_key):
        pass






