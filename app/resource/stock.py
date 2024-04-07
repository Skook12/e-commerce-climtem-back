from flask import Blueprint, jsonify, request
from app.model import Stock
from app.service import StockServices
from http import HTTPStatus

def get_blueprint(srvc: StockServices) -> Blueprint:
    bp = Blueprint("Stock", __name__)
    
    @bp.get('/stock')
    def getStock():
        r = srvc.select()
        return jsonify(r)

    @bp.get('/stock/<int:id>')
    def getStockbyid(id):
        r = srvc.select(id)
        return jsonify(r)
    
    @bp.post('/stock')
    def postStock():
        data = request.json
        r = Stock(
            product_id=data['product_id'],
            amount=data['amount'],
            created_at=data['created_at'],
            updated_at=data['updated_at']
        )
        status = srvc.insert(r.load())
        return jsonify(r), HTTPStatus.CREATED if status == 201 else status
    
    return bp

    