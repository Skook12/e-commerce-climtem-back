from flask import Flask
from .resource import teste

PREFX_API = '/api/v1/'


def create_server():
    '''Starts flask server'''
    app = Flask(__name__)
    #app.config.from_object(config) configs

    app.register_blueprint(teste.get_blueprint(), url_prefix=PREFX_API)

    return app 