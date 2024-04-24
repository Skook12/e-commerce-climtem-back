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
    
    @bp.get('/products/sales/<int:page>')
    def getSales(page):
        query = f'WHERE discount < 1 LIMIT 9'
        if page != None and page != 0:
            query += f' OFFSET {page * 9}'
        r = srvc.select(search=query)
        return jsonify(r)

    @bp.get('/products/query/<int:page>')
    def getProductbyQuery(page):
        params = request.args.get('params[]')
        if params == None:
            params = "{,,}"
        params = params.strip("{}")
        lst = [item.strip() for item in params.split(",")]
        query = f'''p
            JOIN Category c ON ID_Category = c.category_id
            JOIN Brand b ON ID_Brand = b.brand_id
            JOIN product_image i ON p.ID_Product = i.ID_Product
            WHERE c.name ~~* \'{lst[0]}%\' and
            b.name ~~* \'{lst[1]}%\' and 
            p.name ~~* \'{lst[2]}%\'
            ORDER BY p.ID_Product LIMIT 9
        '''
        if page != None and page != 0:
            query += f' OFFSET {page * 9}'
        r = srvc.select(search=query)
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
