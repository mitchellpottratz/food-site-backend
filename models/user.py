import os
import datetime

from peewee import *
from flask_login import UserMixin

DATABASE = SqliteDatabase('foodsite.sqlite')

class User(UserMixin, Model):
    first_name = CharField()
    last_name = CharField()
    email = CharField()
    password = CharField()
    active = BooleanField(default=False)
    last_updated = DateTimeField(default=datetime.datetime.now)
    timestamp = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = DATABASE