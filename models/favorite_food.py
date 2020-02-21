from peewee import *
from .base_food_item import BaseFoodItem
from .user import User


''' 
This model represents a food item that the user favorites
'''


class FavoriteFood(BaseFoodItem):
    user = ForeignKeyField(User, backref='favorite_foods')


    