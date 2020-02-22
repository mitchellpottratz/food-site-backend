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
    food_item_api_key = CharField(max_length=155)
    name = CharField(max_length=155)
    description = CharField(max_length=500, null=True)
    price = FloatField()
    instructions = CharField(max_length=500, null=True)


    



