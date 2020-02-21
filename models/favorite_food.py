from peewee import *
from .base import BaseModel
from .user import User


''' 
This model represents a food item that the user favorites
'''


class FavoriteFood(BaseModel):
    user = ForeignKeyField(User, backref='favorite foods')