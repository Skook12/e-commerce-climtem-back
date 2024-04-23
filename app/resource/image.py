from flask import Blueprint, jsonify
from app.service import StorageService

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

    return bp
