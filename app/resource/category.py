from flask import Blueprint, jsonify, request
from app.security.jwt_utils import admin_required
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
        r = srvc.select(f'WHERE category_id = {id}')
        return jsonify(r)

    @bp.put('/category/<int:id>')
    @admin_required
    def updateCategory(id):
        data = request.json
        srvc.update('name', f'category_id = {id}', f'\'{data["name"]}\'')
        return jsonify({"id": id, "name": data["name"]}), HTTPStatus.OK

    @bp.post('/category')
    @admin_required
    def postCategory():
        data = request.json
        r = Category(name=data['name'])
        status = srvc.insert(r.load())
        return jsonify(r), HTTPStatus.CREATED if status == 201 else status
    
    return bp
