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
from resources.food_items import food_items
from resources.favorite_foods import favorite_foods
from resources.carts import carts
from resources.food_item_customizations import food_item_customizations
from resources.elastic import elastic

# model imports 
from models.base import BaseModel
from models.user import User
from models.address import Address
from models.cart import Cart
from models.base_food_item import BaseFoodItem
from models.food_item import FoodItem
from models.favorite_food import FavoriteFood
from models.food_item_customization import FoodItemCustomization 


# creates an instance of the server
server = Server([[users, '/api/v1/users'],
                 [restaurants, '/api/v1/restaurants'],
                 [addresses, '/api/v1/addresses'],
                 [food_items, '/api/v1/food-items'],
                 [favorite_foods, '/api/v1/favorite-foods'],
                 [carts, '/api/v1/carts'],
                 [food_item_customizations, '/api/v1/food-item-customizations'],
                 [elastic, '/api/v1/elasticsearch']])

# creates an instance of the database                
database = Database([BaseModel, User, Address, Cart, BaseFoodItem, FoodItem, FavoriteFood, FoodItemCustomization])

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
    g.db = database.DATABASE
    g.db.connect()

# closes the database and returnt the response for every request
@app.after_request
def after_request(response):
    g.db.close()
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response


if __name__ == '__main__':
    database.initialize_tables()
    app = server.start()

