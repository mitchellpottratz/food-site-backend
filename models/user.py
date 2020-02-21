from peewee import *
from flask_login import UserMixin
from .base import BaseModel
# from models.food_item import FoodItem 


class User(BaseModel, UserMixin):
    first_name = CharField(max_length=55)
    last_name = CharField(max_length=55)
    email = CharField(max_length=255)
    password = CharField(max_length=255)
    # favorite_foods = ForeignKeyField(FoodItem, backref='food_items')
    active = BooleanField(default=True)
    