import os
from peewee import *
from .base import BaseModel
import requests
import json


''' 
This model is the base class for representing a food item. It contains all the fields 
needed to hold a food item from the EatStreet API.
'''


class BaseFoodItem(BaseModel):
    restaurant_api_key = CharField(max_length=155)
    menu_api_key = CharField(max_length=155)
    food_item_api_key = CharField(max_length=155)
    name = CharField(max_length=155)
    description = CharField(max_length=500, null=True)
    price = DecimalField()
    instructions = CharField(max_length=500, null=True)


    '''
        *** 
        Possible will not need this code below but that'll be ultimately decided when 
        more of the application is developed 
        ***
    ''' 

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




