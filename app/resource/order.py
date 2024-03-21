from flask import Blueprint, jsonify, request
from app.model import Order
from app.service import OrderService
from http import HTTPStatus

def get_blueprint(srvc: OrderService) -> Blueprint:
    bp = Blueprint("Order", __name__)
    
    @bp.get('/order')
    def getOrder():
        order = srvc.select()
        return jsonify(order)

    @bp.get('/order/<int:id>')
    def getOrderbyid(id):
        order = srvc.select(id)
        return jsonify(order)
    
    @bp.post('/order')
    def postOrder():
        data = request.json
        order = Order(
            id=data['id'],
            User_id=data['User_id'],
            buy_date=data['buy_date'],
            status=data['status']
        )
        status = srvc.insert(order.load())
        return jsonify(order), HTTPStatus.CREATED if status == 201 else status
    
    return bp
