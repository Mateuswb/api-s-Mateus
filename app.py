from flask import Flask
from flask_restful import Api
from flask_cors import CORS

from controllers.Mateus import Mateus

app = Flask(__name__)
CORS(app)

api = Api(app)
api.add_resource(Mateus, '/mateus')

if __name__ == '__main__':
    app.run()
