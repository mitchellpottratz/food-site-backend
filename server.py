import os 
from flask import Flask
from flask_login import LoginManager
from flask_cors import CORS

# allows flask to access enviroment variables
from dotenv import load_dotenv
dotenv_path = os.path.join(os.path.dirname(__file__), '.env') 
load_dotenv(dotenv_path)


class Server:
    def __init__(self, blueprints):
        self.app = Flask(__name__)
        self.login_manager = LoginManager()
        self.DEBUG = os.environ['DEBUG']
        self.PORT = os.environ['PORT']
        self.origin = self.set_origin()

        # sets the apps secret key
        self.app.secret_key = os.environ['SECRET_KEY']

        # sets up cors configuration for the flask app
        self.setup_cors()

        # sets up the login manager
        self.setup_login_manager()

        # sets all fo the blueprints in a list
        self.blueprints = blueprints

        # registers all of the blueprints and configures CORS for them
        self.register_blueprints()

    # sets which url is able to access this application
    def set_origin(self):
        if self.DEBUG:
            return 'http://localhost:3000'
        else:
            return os.environ['ORIGIN']

    def setup_cors(self):
        CORS(self.app, resources={r"/*": {"origins": "*"}})

    # sets up flask_login
    def setup_login_manager(self):
        self.login_manager.init_app(self.app)

    # loops through all of the blueprints and registers them with the application
    def register_blueprints(self):
        for blueprint in self.blueprints:
            self.app.register_blueprint(blueprint[0], url_prefix=blueprint[1])
            # CORS(blueprint[0], origins=[self.origin], supports_credentials=True)

    def start(self): 
        print('DEBUG:', self.DEBUG)
        # if the server is running in debug, then the port needs to be specified
        if self.DEBUG:
            self.app.run(debug=self.DEBUG, port=self.PORT)
        # if the server is running in production GCP doesnt need the port passed into the run method
        else: 
            self.app.run()