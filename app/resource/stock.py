from flask import Blueprint, jsonify, request
from app.model import Stock
from app.service import StockServices
from http import HTTPStatus

def get_blueprint(srvc: StockServices) -> Blueprint:
    bp = Blueprint("Stock", __name__)
    
    @bp.get('/stock')
    def getCategory():
        category = srvc.select()
        return jsonify(category)

    @bp.get('/stock/<int:id>')
    def getCategorybyid(id):
        category = srvc.select(id)
        return jsonify(category)
    
    @bp.post('/stock')
    def postCategory():
        data = request.json
        category = Stock(
            id=data['id'],
            product_id=data['product_id'],
           name=data['name']
        )
        status = srvc.insert(category.load())
        return jsonify(category), HTTPStatus.CREATED if status == 201 else status
    
    return bp

    