from flask import Blueprint, jsonify, request
from app.model import Product
from app.service import ProductService
from http import HTTPStatus

def get_blueprint(srvc: ProductService) -> Blueprint:
    bp = Blueprint("Product", __name__)
    
    @bp.get('/products')
    def getProduct():
        r = srvc.select()
        return jsonify(r)

    @bp.get('/products/<int:id>')
    def getProductbyid(id):
        r = srvc.select(f'WHERE ID_Product = {id}')
        return jsonify(r)

    @bp.get('/products/<string:name>/<int:page>')
    def getProductbyName(name, page):
        query = f'WHERE name ~~* \'%{name}%\' ORDER BY ID_Product LIMIT 9'
        if page != None and page != 0:
            query += f' OFFSET {page * 9}'
        r = srvc.select(query)
        return jsonify(r)

    @bp.get('/products/brand/<string:name>/<int:page>')
    def getProductbyBrand(name, page):
        query = f'JOIN Brand b ON ID_Brand = b.brand_id WHERE b.name ~~* \'%{name}%\' ORDER BY ID_Product LIMIT 9'
        if page != None and page != 0:
            query += f' OFFSET {page * 9}'
        r = srvc.select(query)
        return jsonify(r)

    @bp.get('/products/category/<string:name>/<int:page>')
    def getProductbyCategory(name, page):
        query = f'JOIN Category c ON ID_Category = c.category_id WHERE c.name ~~* \'%{name}%\' ORDER BY ID_Product LIMIT 9'
        if page != None and page != 0:
            query += f' OFFSET {page * 9}'
        r = srvc.select(query)
        return jsonify(r)

    @bp.get('/products/query/<string:brand>/<string:cat>/<int:page>')
    def getProductbyBrandCategory(brand, cat, page):
        query = f'p JOIN Category c ON ID_Category = c.category_id JOIN Brand b ON ID_Brand = b.brand_id WHERE c.name ~~* \'%{cat}%\' and b.name ~~* \'%{brand}%\' ORDER BY ID_Product LIMIT 9'
        if page != None and page != 0:
            query += f' OFFSET {page * 9}'
        r = srvc.select(query)
        return jsonify(r)
    
    @bp.get('/products/query/<string:brand>/<string:cat>/<string:search>/<int:page>')
    def getProductbyQuery(brand, cat, search, page):
        query = f'p JOIN Category c ON ID_Category = c.category_id JOIN Brand b ON ID_Brand = b.brand_id WHERE c.name ~~* \'%{cat}%\' and b.name ~~* \'%{brand}%\' and p.name ~~* \'%{search}%\' ORDER BY ID_Product LIMIT 9'
        if page != None and page != 0:
            query += f' OFFSET {page * 9}'
        r = srvc.select(query)
        return jsonify(r)

    @bp.post('/products')
    def postProduct():
        data = request.json
        r = Product(
            brand_id=data['brand_id'],
            category_id=data['category_id'],
            name=data['name'],
            description=data['description'],
            value=data['value'],
            discount=data['discount']            
        )
        status = srvc.insert(r.load())
        return jsonify(r), HTTPStatus.CREATED if status == 201 else status

    return bp
