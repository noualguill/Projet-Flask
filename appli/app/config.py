env = "DEVELOPMENT"
PRODUCTION_SERVER= "127.0.0.1"
API_NAME = "Flask API"
APP_VERSION = "1.0"
API_KEY="toto"
API_URL= 'http://127.0.0.1:5001'



class BaseConfig():
    DEBUG = True

class DevelopmentConfig(BaseConfig):
    SWAGGER_URL = '/api/docs'
    DATA_SWAGGER = 'http://127.0.0.1:5001/swagger'


