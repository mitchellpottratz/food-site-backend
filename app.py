from flask import g
from flask_login import LoginManager

# server and databased
from server import Server
from database import Database

# resource imports
from resources.users import users

# model imports 
from models.user import User

# creates an instance of the server and database
server = Server(True, 3000)
database = Database([User])

# register blueprints herre
server.register_blueprint(users, '/api/v1/users')

# gets the flask app from the server so therefore it can be used 
# as a decorator like: @app
app = server.app

# established connection to the database before every request
@app.before_request
def before_request():
    print('before request called')
    g.db = database.DATABASE
    g.db.connect()

# closes the database and returnt the response for every request
@app.after_request
def after_request(response):
    print('after request called')
    g.db.close()
    return response

if __name__ == '__main__':
    database.initialize_tables()
    server.start()
