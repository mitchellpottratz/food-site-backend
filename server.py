import os 
from flask import Flask

app = Flask(__name__)

class Server:

    def __init__(self, DEBUG, PORT):
        self.app = Flask(__name__)
        self.DEBUG = DEBUG
        self.PORT = PORT

    def register_blueprint(resource, path):
        self.app.register_blueprint(resource, path) 

    def start(self): 
        self.app.run(debug=self.DEBUG, port=self.PORT)
        print("Server is running on port", self.PORT)

    