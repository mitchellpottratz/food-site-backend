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






