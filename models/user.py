from peewee import *
from flask_login import UserMixin
from .base import BaseModel


class User(BaseModel, UserMixin):
    first_name = CharField()
    last_name = CharField()
    email = CharField()
    password = CharField()
    active = BooleanField(default=True)
    