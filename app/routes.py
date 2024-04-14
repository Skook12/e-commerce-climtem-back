from flask import Flask
from .resource import (
    user,
    address,
    brand,
    category,
    image,
    order,
    stock,
    product
)
from .service import (
    UserService,
    AddressService,
    BrandService,
    CategoryService,
    OrderService,
    ProductService,
    StockServices,
    ImageService,
    StorageService
)
from .db import connection

PREFX_API = '/api/v1/'


def create_server(config):
    '''Starts flask server'''
    app = Flask(__name__)
    db = connection.getConnection(config.PSQL_SETTINGS)
    storage = StorageService(db)

    userService = UserService(db)
    app.register_blueprint(user.get_blueprint(userService), url_prefix=PREFX_API)

    addressService = AddressService(db)
    app.register_blueprint(address.get_blueprint(addressService), url_prefix=PREFX_API)
    
    brandService = BrandService(db)
    app.register_blueprint(brand.get_blueprint(brandService), url_prefix=PREFX_API)
    
    categoryService = CategoryService(db)
    app.register_blueprint(category.get_blueprint(categoryService), url_prefix=PREFX_API)
    
    orderService = OrderService(db)
    app.register_blueprint(order.get_blueprint(orderService), url_prefix=PREFX_API)
    
    productService = ProductService(db)
    app.register_blueprint(product.get_blueprint(productService, storage), url_prefix=PREFX_API)
    
    stockServices = StockServices(db)
    app.register_blueprint(stock.get_blueprint(stockServices), url_prefix=PREFX_API)
    
    imageService = ImageService(db)
    app.register_blueprint(image.get_blueprint(imageService), url_prefix=PREFX_API)

    return app
