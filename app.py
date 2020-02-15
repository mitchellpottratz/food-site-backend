# import flask
from flask import g

# server and databased
from server import Server
from database import Database

# resource imports
from resources.users import users

# model imports 
from models.user import User

from flask_login import LoginManager

server = Server(True, 3000)
database = Database([User])

# register blueprints
server.register_blueprint(users, '/api/v1/users')

app = server.app

@app.before_request
def before_request():
    g.db = database.DATABASE
    g.db.connect()

@app.after_request
def after_request(response):
    g.db.close()
    return response

if __name__ == '__main__':
    database.initialize_tables()
    server.start()
