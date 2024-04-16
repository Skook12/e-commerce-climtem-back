from flask import Blueprint, jsonify, request
from app.model import Image
from app.service import StorageService
from http import HTTPStatus

def get_blueprint(srvc: StorageService) -> Blueprint:
    bp = Blueprint("Image", __name__)
    
    @bp.get('/images')
    def getImage():
        image = srvc.select()
        return jsonify(image)

    @bp.get('/images/<int:id>')
    def getImagebyid(id):
        image = srvc.select(id)
        return jsonify(image)
    
    @bp.post('/images')
    def postImage():
        data = request.form['product']
        file = request.files['file']
        st = srvc.loadFile(file)    
        r = Image(
            product_id=data,
            path=st
        )
        status = srvc.insert(r.load())
        return jsonify(st), HTTPStatus.CREATED if status == 201 else status
    
    return bp
