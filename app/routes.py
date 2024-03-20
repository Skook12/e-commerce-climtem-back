from flask import Flask
from .resource import (
    user,
    address,
    brand
)
from .service import (
    UserService,
    AddressService,
    BrandService
)
from .db import connection

PREFX_API = '/api/v1/'


def create_server(config):
    '''Starts flask server'''
    app = Flask(__name__)
    db = connection.getConnection(config.PSQL_SETTINGS)

    userService = UserService(db)
    app.register_blueprint(user.get_blueprint(userService), url_prefix=PREFX_API)

    addressService = AddressService(db)
    app.register_blueprint(address.get_blueprint(addressService), url_prefix=PREFX_API)
    
    brandService = BrandService(db)
    app.register_blueprint(brand.get_blueprint(brandService), url_prefix=PREFX_API)

    return app