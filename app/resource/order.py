from flask import Blueprint, jsonify, request
from app.security.jwt_utils import admin_required
from app.model import Order
from app.service import OrderService
from http import HTTPStatus

def get_blueprint(srvc: OrderService) -> Blueprint:
    bp = Blueprint("Order", __name__)
    
    @bp.get('/order')
    def getOrder():
        r = srvc.select()
        return jsonify(r)

    @bp.get('/order/<int:id>')
    def getOrderbyid(id):
        r = srvc.select(f'ID_Order = {id}')
        return jsonify(r)

    @bp.post('/order')
    @admin_required
    def postOrder():
        data = request.json
        r = Order(
            user_id=data['user_id'],
            buy_date=data['buy_date'],
            status=data['status']
        )
        status = srvc.insert(r.load())
        return jsonify(r), HTTPStatus.CREATED if status == 201 else status
    
    return bp
