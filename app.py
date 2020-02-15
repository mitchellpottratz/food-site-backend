# import flask
from flask import Flask

# server and databased
from server import Server
from database import Database

# resource imports
from resources.users import users

from flask_login import LoginManager

app = Flask(__name__)


server = Server(True, 3000)
database = Database([])

# register blueprint
server.register_blueprint(users, '/api/v1/users')


if __name__ == '__main__':
    database.initialize_tables()
    server.start()
