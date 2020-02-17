from peewee import *
from .base import BaseModel
from .user import User

''' 
This model is a a delivery address the user can save. Users are able to have multiple
delivery addresses which can be given a name.
'''

class Address(BaseModel):
    user = ForeignKeyField(User, backref='addresses')
    name = CharField(max_length=55)
    address = CharField(max_length=255)
    instructions = CharField(max_length=300)



