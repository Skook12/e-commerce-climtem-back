from flask import Blueprint, jsonify, request
from app.security.jwt_utils import token_required
from app.model import Order, ShoppingCar
from app.service import OrderService, ShoppingCarService
from http import HTTPStatus

def get_blueprint(srvc: OrderService, carsrvc: ShoppingCarService) -> Blueprint:
    bp = Blueprint("Order", __name__)
    
    @bp.get('/order')
    def getOrder():
        r = srvc.select()
        return jsonify(r)

    @bp.get('/order/<int:id>')
    def getOrderbyid(id):
        r = srvc.select(f'ID_Order = {id}')
        return jsonify(r)

    @bp.post('/order/<int:id>')
    # @token_required
    def postOrder(id):
        data = request.json
        r = Order(
            user_id=id,
            buy_date=data['buy_date'],
            status=data['status'],
            payment_type=data['payment_type'],
            expiration=data['expiration'],
            total_bought=data['total']
        )
        order_id = srvc.insert(r.load())

        for p in list(data['products']):
            shoppingcar = ShoppingCar(order_id, p['product_id'], p['quantity'])
            status = carsrvc.insert(shoppingcar.load())
            
        return jsonify(r), HTTPStatus.CREATED if status == 201 else status
    
    return bp
