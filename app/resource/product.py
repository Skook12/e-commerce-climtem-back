from flask import Blueprint, jsonify, request
from app.model import Product
from app.service import ProductService
from http import HTTPStatus

def get_blueprint(srvc: ProductService) -> Blueprint:
    bp = Blueprint("Product", __name__)
    
    @bp.get('/product')
    def getOrder():
        order = srvc.select()
        return jsonify(order)

    @bp.get('/product/<int:id>')
    def getOrderbyid(id):
        order = srvc.select(id)
        return jsonify(order)
    
    @bp.post('/product')
    def postOrder():
        data = request.json
        order = Product(
            User_id=data['User_id'],
            buy_date=data['buy_date'],
            status=data['status']
        )
        status = srvc.insert(order.load())
        return jsonify(order), HTTPStatus.CREATED if status == 201 else status
    
    return bp
