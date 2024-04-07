from flask import Blueprint, jsonify, request
from app.model import Category
from app.service import CategoryService
from http import HTTPStatus

def get_blueprint(srvc: CategoryService) -> Blueprint:
    bp = Blueprint("Category", __name__)
    
    @bp.get('/category')
    def getCategory():
        r = srvc.select()
        return jsonify(r)

    @bp.get('/category/<int:id>')
    def getCategorybyid(id):
        r = srvc.select(id)
        return jsonify(r)
    
    @bp.post('/category')
    def postCategory():
        data = request.json
        r = Category(
           name=data['name']
        )
        status = srvc.insert(r.load())
        return jsonify(r), HTTPStatus.CREATED if status == 201 else status
    
    return bp
