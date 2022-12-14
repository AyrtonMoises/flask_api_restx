from flask import Flask, Blueprint
from flask_restx import Api


class Server():

    def __init__(self):
        self.app = Flask(__name__)
        self.blueprint = Blueprint('api', __name__, url_prefix='/api')
        self.api = Api(
            self.blueprint,
            version='1.0',
            title="Sample Book API",
            description='A simple book API',
            doc='/doc'
        )
        self.app.register_blueprint(self.blueprint)

        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
        self.app.config['PROPAGATE_EXCEPTIONS'] = True
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    def run(self):
        self.app.run(
            port=5000,
            host='0.0.0.0',
            debug=True
        )

    
server = Server()