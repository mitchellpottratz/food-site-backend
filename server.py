import os 
from flask import Flask
from flask_login import LoginManager, current_user

from dotenv import load_dotenv

# allows flask to access enviroment variables
dotenv_path = os.path.join(os.path.dirname(__file__), '.env') 
load_dotenv(dotenv_path)


class Server:

    def __init__(self, DEBUG, PORT):
        self.app = Flask(__name__)
        self.login_manager = LoginManager()
        self.DEBUG = DEBUG
        self.PORT = PORT

        # sets the apps secret key
        self.app.secret_key = os.environ['SECRET_KEY']

        # sets up the login manager
        self.setup_login_manager()

    def setup_login_manager(self):
        self.login_manager.init_app(self.app)

    def register_blueprint(self, resource, path):
        self.app.register_blueprint(resource, url_prefix=path) 


    def start(self): 
        self.app.run(debug=self.DEBUG, port=self.PORT)
        print("Server is running on port", self.PORT)

    