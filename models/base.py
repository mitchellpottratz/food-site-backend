import datetime
from peewee import *

DATABASE = SqliteDatabase('foodsite.sqlite')

''' 
All other models will inherit from BaseModel. Therefore all models will automatically have a last_updated
and timestamp field, also they will have the meta class information which connects to the database.
'''

class BaseModel(Model):
    last_updated = DateTimeField(default=datetime.datetime.now)
    timestamp = DateTimeField(default=datetime.datetime.now)

    class Meta: 
        database = DATABASE

