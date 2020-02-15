# import flask
from flask import Flask

# server and databased
from server import Server
from database import Database

# resource imports
from resources.users import users

from flask_login import LoginManager


server = Server(True, 3000)
database = Database([])

# register blueprints
server.register_blueprint(users, '/api/v1/users')


if __name__ == '__main__':
    database.initialize_tables()
    server.start()
