from flask import Blueprint, jsonify, request
from app.model import Brand
from app.service import BrandService
from http import HTTPStatus

def get_blueprint(srvc: BrandService) -> Blueprint:
    bp = Blueprint("Brand", __name__)
    
    @bp.get('/brand')
    def getBrand():
        r = srvc.select()
        return jsonify(r)

    @bp.get('/brand/<int:id>')
    def getBrandbyid(id):
        r = srvc.select(f'brand_id = {id}')
        return jsonify(r)
    
    @bp.post('/brand')
    def postBrand():
        data = request.json
        r = Brand(name = data['name'])
        status = srvc.insert(r.load())
        return jsonify(r), HTTPStatus.CREATED if status == 201 else status
    
    return bp
