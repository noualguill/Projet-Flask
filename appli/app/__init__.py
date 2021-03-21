from flask import Flask, jsonify
from flask_restful import Api
from flask_swagger import swagger
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS


# Declare the flask app and wrap it in API
app = Flask(__name__)
api = Api(app)

from app import config
from app import routes

if config.env == "DEVELOPMENT":
    conf = config.DevelopmentConfig
app.config.from_object(conf)
cors = CORS(app, resources={r"/*": {"origins": "*"}})


"""
    Swagger
"""
@app.route("/swagger")
def swaggerController():
    swag = swagger(app)
    swag['info']['version'] = config.APP_VERSION
    swag['info']['title'] = config.API_NAME
    return jsonify(swag)

swaggerui_blueprint = get_swaggerui_blueprint(
    conf.SWAGGER_URL,
    conf.DATA_SWAGGER,
    config = {
        'app_name': "Flask API"
    },
)
app.register_blueprint(swaggerui_blueprint, url_prefix = conf.SWAGGER_URL)