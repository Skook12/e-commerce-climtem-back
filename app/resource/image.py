from flask import Blueprint, jsonify
from app.service import StorageService

def get_blueprint(srvc: StorageService) -> Blueprint:
    bp = Blueprint("Image", __name__)
    
    @bp.get('/images')
    def getImage():
        image = srvc.select()
        return jsonify(image)

    @bp.get('products/images/<int:product_id>')
    def getImagebyid(product_id):
        image = srvc.select(product_id)
        return jsonify(image)

    return bp
