from flask import Blueprint, jsonify, request
from app.model import Product, Image
from app.service import ProductService, StorageService
from http import HTTPStatus

def get_blueprint(srvc: ProductService, strg: StorageService) -> Blueprint:
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
    
    @bp.get('/products/query/brand/<string:brand>/<string:search>/<int:page>')
    def getProductbyBrandSearch(brand, search, page):
        query = f'p JOIN Brand b ON ID_Brand = b.brand_id WHERE p.name ~~* \'%{search}%\' and b.name ~~* \'%{brand}%\' ORDER BY ID_Product LIMIT 9'
        if page != None and page != 0:
            query += f' OFFSET {page * 9}'
        r = srvc.select(query)
        return jsonify(r)
    
    @bp.get('/products/query/category/<string:cat>/<string:search>/<int:page>')
    def getProductbyCategorySearch(cat, search, page):
        query = f'p JOIN Category c ON ID_Category = c.category_id WHERE c.name ~~* \'%{cat}%\' and p.name ~~* \'%{search}%\' ORDER BY ID_Product LIMIT 9'
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
        file = request.files['file']
        st = strg.loadFile(file)
        r = Product(
            brand_id=request.form['brand_id'],
            category_id=request.form['category_id'],
            name=request.form['name'],
            description=request.form['description'],
            value=request.form['value'],
            discount=request.form['discount']
        )
        id = int(srvc.insert(r.load()))
        i = Image(
            product_id=id,
            path=st
        )
        status = strg.insert(i.load())
        return jsonify(r), HTTPStatus.CREATED if status == 201 else status

    return bp
