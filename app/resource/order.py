from flask import Blueprint, jsonify, request
from app.security.jwt_utils import admin_required, token_required
from app.model import Order, ShoppingCar, OrderStatus, PaymentType
from datetime import datetime
from app.service import OrderService, ShoppingCarService
from http import HTTPStatus

def get_blueprint(srvc: OrderService, carsrvc: ShoppingCarService) -> Blueprint:
    bp = Blueprint("Order", __name__)
    
    @bp.get('/order')
    @admin_required
    def getOrder():
        r = srvc.select()
        return jsonify(r)

    @bp.get('/order/<int:id>')
    @token_required
    def getOrderbyid(id):
        query = f"""
            o JOIN Products_Order po
            ON o.ID_Order = po.ID_Order
            JOIN Product p 
            ON po.ID_Product = p.ID_Product
            JOIN Product_Image i
            ON i.ID_Product = p.ID_Product
            WHERE ID_User = {id}
        """
        r = srvc.select(query)
        return jsonify(r)

    @bp.post('/order/<int:id>')
    @token_required
    def postOrder(id):
        data = request.json
        r = Order(
            user_id=id,
            buy_date=datetime.now(),
            status=OrderStatus.Payment_Pending.value,
            payment_type=PaymentType(data['payment_type']).value,
            expiration=datetime.today(),
            total_bought=data['total']
        )
        order_id = srvc.insert(r.load())

        for p in list(data['products']):
            shoppingcar = ShoppingCar(order_id, p['product_id'], p['quantity'])
            status = carsrvc.insert(shoppingcar.load())
            
        return jsonify(r), HTTPStatus.CREATED if status == 201 else status
    
    return bp
