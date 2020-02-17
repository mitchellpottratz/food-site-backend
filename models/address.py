from peewee import *
from .base import BaseModel
from .user import User

''' 
This model is a a delivery address the user can save. Users are able to have multiple
delivery addresses which they can give names to
'''

class Address(BaseModel):
    user = ForeignKeyField(User, backref='addresses')
    name = CharField(max_length=55)
    state = CharField(max_length=25)
    city = CharField(max_length=55)
    street = CharField(max_length=155)
    house_number = IntegerField(null=True)
    apartment_number = IntegerField(null=True)
    instructions = CharField(max_length=300)



