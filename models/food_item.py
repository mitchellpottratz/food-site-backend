from peewee import *
from .base_food_item import BaseFoodItem
from .cart import Cart


''' 
This model represents a food item that is in a users cart from the EatStreet api 
'''


class FoodItem(BaseFoodItem):
    cart = ForeignKeyField(Cart, backref='food_items')







