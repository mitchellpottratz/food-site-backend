# import flask
from flask import Flask

# server and databased
from server import Server
from database import Database
server = Server(True, 3000)
database = Database([])

# resource imports
from resources.users import User

from flask_login import LoginManager

app = Flask(__name__)

# api endpoint route
app.register_blueprint(User, url_prefix='/api/v1/users')

if __name__ == '__main__':
    database.initialize_tables()
    server.start()
