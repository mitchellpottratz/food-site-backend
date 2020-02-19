from peewee import *
from .base import BaseModel
from .cart import Cart


class FoodItem(BaseModel):
    cart = ForeignKeyField(Cart, backref='food-items')
    name = CharField(max_length=155)
    price = DecimalField()

    



