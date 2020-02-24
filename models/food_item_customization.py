from peewee import *

from .base import BaseModel
from .base_food_item import BaseFoodItem


''' 
This model respresents a food item customization from the EatStreet API
'''


class FoodItemCustomization(BaseModel):
    food_item = ForeignKeyField(BaseFoodItem, backref='customizations')
    api_key = CharField(max_length=155)
    name = CharField(max_length=155)
    price = FloatField()
    count = IntegerField(null=True)





