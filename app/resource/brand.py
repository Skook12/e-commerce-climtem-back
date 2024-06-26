from flask import Blueprint, jsonify, request
from app.security.jwt_utils import admin_required
from app.model import Brand
from app.service import BrandService
from http import HTTPStatus

def get_blueprint(srvc: BrandService) -> Blueprint:
    bp = Blueprint("Brand", __name__)
    
    @bp.get('/brand')
    def getBrand():
        r = srvc.select()
        return jsonify(r)

    @bp.get('/brands/<int:page>')
    def getBrands(page):
        params = request.args.get('params[]')
        query = ''
        if params != None:
            params = params.strip("{}")
            query = f'WHERE name ~~* \'{params}%\' '

        query += f'LIMIT 9'
        if page != None and page != 0:
            query += f' OFFSET {page * 9}'
        r = srvc.select(query)
        return jsonify(r)

    @bp.get('/brand/<int:id>')
    def getBrandbyid(id):
        r = srvc.select(f'WHERE brand_id = {id}')
        return jsonify(r)

    @bp.put('/brand/<int:id>')
    @admin_required
    def updateBrand(id):
        data = request.json
        srvc.update('name', f'brand_id = {id}', f'\'{data["name"]}\'')
        return jsonify({"id": id, "name": data["name"]}), HTTPStatus.OK

    @bp.delete('/brand/<int:id>')
    @admin_required
    def deleteBrand(id):
        srvc.delete(id)
        return jsonify({"msg": f'{id} Deleted.'}), HTTPStatus.OK

    @bp.post('/brand')
    @admin_required
    def postBrand():
        data = request.json
        r = Brand(name = data['name'])
        status = srvc.insert(r.load())
        return jsonify(r), HTTPStatus.CREATED if status == 201 else status
    
    return bp
