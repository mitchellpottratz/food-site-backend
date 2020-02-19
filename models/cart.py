from peewee import *
from .base import BaseModel
from .user import User


class Cart(BaseModel):
    user = ForeignKeyField(User, backref='cart', unique=True)

    # checks if the user id in the parameters is the user of the model instance
    def user_is_owner(self, user_id):
        if self.user.id != user_id:
            return False
        return True

