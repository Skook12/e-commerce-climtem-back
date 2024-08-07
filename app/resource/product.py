from flask import Blueprint, jsonify, request
from app.security.jwt_utils import admin_required
from app.model import Product, Image
from app.service import ProductService, StorageService, calulateFreight,calulateMutipleFreight
from http import HTTPStatus

def get_blueprint(srvc: ProductService, strg: StorageService ) -> Blueprint:
    bp = Blueprint("Product", __name__)
    
    @bp.get('/products')
    def getProduct():
        r = srvc.select(f'p JOIN product_image i ON p.ID_Product = i.ID_Product')
        return jsonify(r)

    @bp.get('/products/<int:id>')
    def getProductbyid(id):
        r = srvc.select(f'p JOIN product_image i ON p.ID_Product = i.ID_Product WHERE p.ID_Product = {id} ORDER BY p.ID_Product')
        return jsonify(r)
    
    @bp.get('/products/freight/<int:id>/<int:cep>')
    def getProductbyFreightid(id,cep):
        r = srvc.select(f'p JOIN product_image i ON p.ID_Product = i.ID_Product WHERE p.ID_Product = {id} ORDER BY p.ID_Product')
        return calulateFreight(r,cep)
    
    @bp.post('/products/mutiplefreight/<int:cep>')
    def getProductbyMutipleFreightid(cep):
        products = []
        json = request.json
        jsonList = list(json['products'])
        for j in jsonList:
            r = srvc.select(f'p JOIN product_image i ON p.ID_Product = i.ID_Product WHERE p.ID_Product = {j["product_id"]} ORDER BY p.ID_Product')
            products.append([r[0], j['quantity']])     
        return calulateMutipleFreight(products,cep)
    
    @bp.get('/products/sales')
    def getSales():       
        r = srvc.select( f'WHERE discount < 1')
        return jsonify(r)

    @bp.get('/products/sales/<int:page>')
    def getSalesPage(page):
        query = f'p JOIN product_image i ON p.ID_Product = i.ID_Product WHERE discount < 1 LIMIT 4'
        if page != None and page != 0:
            query += f' OFFSET {page * 4}'
        r = srvc.select(search=query)
        return jsonify(r)

    @bp.get('/products/highlights/<int:page>')
    def getHighlightPage(page):
        query = f'p JOIN product_image i ON p.ID_Product = i.ID_Product WHERE p.highl = True LIMIT 4'
        if page != None and page != 0:
            query += f' OFFSET {page * 4}'
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
    @admin_required
    def postProduct():
        file = request.files['file']
        st = strg.loadFile(file)
        r = Product(
            ID_Brand=request.form['brand_id'],
            ID_Category=request.form['category_id'],
            name=request.form['name'],
            description=request.form['description'],
            value=request.form['value'],
            discount=request.form['discount'],
            highl=request.form['highlight'],
            height=request.form['height'],
            width=request.form['width'],
            length=request.form['length'],
            weight=request.form['weight'],
            quantity=request.form['quantity']
        )
        id = int(srvc.insert(r.load()))
        i = Image(
            product_id=id,
            path=st
        )
        status = strg.insert(i.load())
        return jsonify(r), HTTPStatus.CREATED if status == 201 else status
   
    @bp.put('/products/<int:id>')
    @admin_required
    def putProduct(id):
        hasFile = True
        try:
            file = request.files['file']
        except Exception as e:
            hasFile = False

        r = Product(
            ID_Brand=request.form['brand_id'],
            ID_Category=request.form['category_id'],
            name=request.form['name'],
            description=request.form['description'],
            value=request.form['value'],
            discount=request.form['discount'],
            highl=request.form['highlight'],
            height=request.form['height'],
            width=request.form['width'],
            length=request.form['length'],
            weight=request.form['weight'],
            quantity=request.form['quantity']
        )
        for attr, val in vars(r).items():
            srvc.update(attr, f'ID_Product = {id}', val)

        if hasFile:
            st = strg.loadFile(file)
            strg.update("path", f'ID_Product = {id}', f'\'{st}\'')

        return jsonify(r), HTTPStatus.OK

    @bp.delete('/products/<int:id>')
    @admin_required
    def deleteProduct(id):
        strg.delete(id)
        srvc.delete(id)
        return jsonify({"msg": f'{id} Deleted.'}), HTTPStatus.OK

    return bp
