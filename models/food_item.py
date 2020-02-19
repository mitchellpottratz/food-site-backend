import os
from peewee import *
from .base import BaseModel
from .cart import Cart
import requests
import json

''' 
This model represents a food item that is in a users cart from the EatStreet api 
'''

class FoodItem(BaseModel):
    cart = ForeignKeyField(Cart, backref='food-items')
    restaurant_api_key = CharField(max_length=155)
    menu_api_key = CharField(max_length=155)
    food_item_api_key = CharField(max_length=155)
    name = CharField(max_length=155)
    description = CharField(max_length=500)
    price = DecimalField()
    instructions = CharField(max_length=500)

    # the api url to search for a restaurants menu
    API_URL = 'https://eatstreet.com/publicapi/v1/restaurant/'

    # header that needs to be sent in the request to the EatStreet api
    API_HEADER = {'X-Access-Token': os.environ['API_KEY']}

    # this method makes a request to the EatStreet api to check if the provided
    # food item api key matches a valid food item
    @staticmethod
    def get_food_item(restaurant_api_key, food_item_api_key):
        response = requests.get(FoodItem.API_URL + restaurant_api_key +
                                '/menu', headers=FoodItem.API_HEADER)

        parsed_response = response.json()
        print('api response:', response)
        
        return parsed_response





