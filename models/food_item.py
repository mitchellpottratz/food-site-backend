from peewee import *
from .base import BaseModel
from .cart import Cart


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
    quantity = IntegerField()

    # the api url to search for a restaurants menu
    API_URL = 'https://eatstreet.com/publicapi/v1/restaurant/'

    # this method makes a request to the EatStreet api to check if the provided
    # food item api key matches a valid food item
    @staticmethod
    def does_food_item_exist(restuarant_api_key, food_item_api_key):
        






