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

# model imports 
from models.base import BaseModel
from models.user import User

# creates an instance of the server and database

# ** blueprints get passed into the Server constructor as a nested list
# ** Example: [ [blueprint name, blueprint path],
#               [another blueprint name, another blueprint path] 
#             ]
server = Server(True, 8000, [[users, '/api/v1/users'],
                             [restaurants, '/api/v1/restaurants']])
database = Database([BaseModel, User])

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
    return response


if __name__ == '__main__':
    database.initialize_tables()
    server.start()
