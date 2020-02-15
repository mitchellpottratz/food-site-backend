import os 
from flask import Flask
from flask_login import LoginManager

# allows flask to access enviroment variables
from dotenv import load_dotenv
dotenv_path = os.path.join(os.path.dirname(__file__), '.env') 
load_dotenv(dotenv_path)


class Server:

    def __init__(self, DEBUG, PORT, resources):
        self.app = Flask(__name__)
        self.login_manager = LoginManager()
        self.DEBUG = DEBUG
        self.PORT = PORT
        self.origin = self.set_origin()

        # sets the apps secret key
        self.app.secret_key = os.environ['SECRET_KEY']

        # sets up the login manager
        self.setup_login_manager()

        self.resources = resources

    # sets which url is able to access this application
    def set_origin(self):
        if self.DEBUG:
            return 'http://localhost:3000'
        else:
            return os.environ['ORIGIN']

    # sets up flask_login
    def setup_login_manager(self):
        self.login_manager.init_app(self.app)

    def register_blueprint(self, resource, path):
        self.app.register_blueprint(resource, url_prefix=path) 

    def register_cors(self):
        pass

    def start(self): 
        self.app.run(debug=self.DEBUG, port=self.PORT)
        print("Server is running on port", self.PORT)

    