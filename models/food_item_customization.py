from peewee import *

from .base import BaseModel
from .food_item import FoodItem


''' 
This model respresents a food item customization from the EatStreet API
'''


class FoodItemCustomization(BaseModel):
    food_item = ForeignKeyField(FoodItem, backref='customizations')
    selection_api_key = CharField(max_length=155)
    choice_api_key = CharField(max_length=155)
    selection_name = CharField(max_length=255)
    choice_name = CharField(max_length=255)
    price = FloatField()
    count = IntegerField(null=True)





