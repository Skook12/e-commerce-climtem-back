from flask import Blueprint, jsonify, request
from app.model import Product, Image
from app.service import (
    ProductService,
    StorageService
)
from http import HTTPStatus

def get_blueprint(srvc: ProductService, storage: StorageService) -> Blueprint:
    bp = Blueprint("Product", __name__)
    
    @bp.get('/product')
    def getProduct():
        r = srvc.select()
        return jsonify(r)

    @bp.get('/product/<int:id>')
    def getProductbyid(id):
        r = srvc.select(id)
        return jsonify(r)
    
    @bp.post('/product')
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
    
    @bp.post('/product/image')
    def postProductImages():
        data = request.form['product']
        path = request.form['path']
        file = request.files['file']
        r = Image(
            product_id=data,
            path=path
        )
        status = 201#storage.insert(r.load())
        st = storage.loadFile(file, path)    
        return jsonify(st), HTTPStatus.CREATED if status == 201 else status
    
    return bp
