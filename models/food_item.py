from peewee import *
from .base import BaseModel
from .cart import Cart


class FoodItem(BaseModel):
    cart = ForeignKeyField(Cart, backref='food-items')
    api_key = CharField(max_length=55)
    name = CharField(max_length=155)
    description = CharField(max_length=500)
    price = DecimalField()






