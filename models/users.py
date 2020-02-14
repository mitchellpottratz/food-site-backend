import os
import datetime

from peewee import *

database = Database([])

from flask_login import UserMixin


class User(UserMixin, Model):
    first_name = CharField()
    last_name = CharField()
    email = CharField()
    password = CharField()
    active = BooleanField(default=False)
    last_updated = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = database 