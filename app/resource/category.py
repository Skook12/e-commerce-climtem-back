from flask import Blueprint, jsonify, request
from app.model import Category
from app.service import CategoryService
from http import HTTPStatus

def get_blueprint(srvc: CategoryService) -> Blueprint:
    bp = Blueprint("Category", __name__)
    
    @bp.get('/category')
    def getCategory():
        category = srvc.select()
        return jsonify(category)

    @bp.get('/category/<int:id>')
    def getCategorybyid(id):
        category = srvc.select(id)
        return jsonify(category)
    
    @bp.post('/category')
    def postCategory():
        data = request.json
        category = Category(
           name=data['name']
        )
        status = srvc.insert(category.load())
        return jsonify(category), HTTPStatus.CREATED if status == 201 else status
    
    return bp
