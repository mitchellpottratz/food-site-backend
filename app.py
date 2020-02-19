print('in app.py file')

from flask import g
from flask_login import current_user
from models.user import User
from peewee import DoesNotExist
from flask_cors import CORS

# server and databased
from server import Server
from database import Database

# resource imports
from resources.users import users
from resources.restaurants import restaurants
from resources.addresses import addresses

# model imports 
from models.base import BaseModel
from models.user import User
from models.address import Address
from models.cart import Cart
from models.food_item import FoodItem

# creates an instance of the server and database
server = Server([[users, '/api/v1/users'],
                 [restaurants, '/api/v1/restaurants'],
                 [addresses, '/api/v1/addresses']])
database = Database([BaseModel, User, Address, Cart, FoodItem])

# gets the app and login_manager objects from the server class so 
# their decorators can be used: @app and @login_manager
app = server.app
login_manager = server.login_manager

# required by flask_login for loading users
@login_manager.user_loader
def load_user(user_id):
    try:
        return User.get(User.id == user_id)
    except DoesNotExist:
        return None

# established connection to the database before every request
@app.before_request
def before_request():
    print('before request')
    g.db = database.DATABASE
    g.db.connect()

# closes the database and returnt the response for every request
@app.after_request
def after_request(response):
    print('after request')
    g.db.close()
    return response


if __name__ == '__main__':
    print('application started')
    database.initialize_tables()
    app = server.start()

