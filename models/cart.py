from peewee import *
from .base import BaseModel
from .user import User


class Cart(BaseModel):
    user = ForeignKeyField(User, backref='cart', unique=True)

