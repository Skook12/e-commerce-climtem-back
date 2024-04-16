from flask import Blueprint, jsonify, request
from app.model import Product
from app.service import ProductService
from http import HTTPStatus

def get_blueprint(srvc: ProductService) -> Blueprint:
    bp = Blueprint("Product", __name__)
    
    @bp.get('/products')
    def getProduct():
        r = srvc.select()
        return jsonify(r)

    @bp.get('/products/brand/<string:name>')
    def getProductbyBrand(name):
        r = srvc.select(f'JOIN Brand b ON ID_Brand = b.brand_id WHERE b.name ~~* \'{name}\'')
        return jsonify(r)

    @bp.get('/products/category/<string:name>')
    def getProductbyCategory(name):
        r = srvc.select(f'JOIN Category c ON ID_Category = c.category_id WHERE c.name ~~* \'{name}\'')
        return jsonify(r)

    @bp.get('/products/<int:id>')
    def getProductbyid(id):
        r = srvc.select(f'WHERE ID_Product = {id}')
        return jsonify(r)
    
    @bp.post('/products')
    def postProduct():
        data = request.json
        r = Product(
            brand_id=data['brand_id'],
            category_id=data['category_id'],
            name=data['name'],
            description=data['description'],
            value=data['value'],
            discount=data['discount']            
        )
        status = srvc.insert(r.load())
        return jsonify(r), HTTPStatus.CREATED if status == 201 else status

    return bp
