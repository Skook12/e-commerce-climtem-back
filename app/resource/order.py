from flask import Blueprint, jsonify, request
from app.security.jwt_utils import admin_required, token_required
from app.model import Order, ShoppingCar, OrderStatus, PaymentType
from datetime import datetime
from app.service import OrderService, ShoppingCarService
from http import HTTPStatus

def get_blueprint(srvc: OrderService, carsrvc: ShoppingCarService) -> Blueprint:
    bp = Blueprint("Order", __name__)
    
    @bp.get('/order/<int:page>')
    @admin_required
    def getOrder(page):
        params = request.args.get('params[]')
        query = f"""
            o JOIN Products_Order po
            ON o.ID_Order = po.ID_Order
            JOIN Product p 
            ON po.ID_Product = p.ID_Product
            JOIN Product_Image i
            ON i.ID_Product = p.ID_Product
            JOIN UserTable u
            ON o.ID_User = u.ID_User
            JOIN User_Address a
            ON o.ID_User = a.ID_User
        """
        if params != None:
            params = params.strip("{}")
            query += f'WHERE u.cpf ~~* \'{params}%\' '

        query += "ORDER BY o.ID_User LIMIT 9"
        if page != None and page != 0:
            query += f' OFFSET {page * 9}'
        r = srvc.select(query)
        return jsonify(r)

    @bp.get('/order/<int:id>/<int:page>')
    @token_required
    def getOrderbyid(id, page):
        query = f"""
            o JOIN Products_Order po
            ON o.ID_Order = po.ID_Order
            JOIN Product p 
            ON po.ID_Product = p.ID_Product
            JOIN Product_Image i
            ON i.ID_Product = p.ID_Product
            JOIN UserTable u
            ON o.ID_User = u.ID_User
            JOIN User_Address a
            ON o.ID_User = a.ID_User
            WHERE o.ID_User = {id}
            ORDER BY o.ID_User LIMIT 9
        """
        if page != None and page != 0:
            query += f' OFFSET {page * 9}'
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
    
    @bp.put('/order/<int:id>')
    @admin_required
    def putStatus(id):
        data = request.json
        r = srvc.update('status', f'ID_Order = {id}', f'\'{OrderStatus(data["status"]).value}\'')
        return jsonify(r)

    return bp
