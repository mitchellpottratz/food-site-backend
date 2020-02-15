import os 
from flask import Flask
from flask_login import LoginManager, current_user

class Server:

    def __init__(self, DEBUG, PORT):
        self.app = Flask(__name__)
        self.login_manager = LoginManager()
        self.DEBUG = DEBUG
        self.PORT = PORT

        # sets the apps secret key
        self.app.secet_key = self.set_secret_key()

        # sets up the login manager
        self.setup_login_manager()

    def set_secret_key(self):
        return os.environ['SECRET_KEY']

    def setup_login_manager(self):
        self.login_manager.init_app(self.app)

    def register_blueprint(self, resource, path):
        self.app.register_blueprint(resource, url_prefix=path) 


    def start(self): 
        self.app.run(debug=self.DEBUG, port=self.PORT)
        print("Server is running on port", self.PORT)

    