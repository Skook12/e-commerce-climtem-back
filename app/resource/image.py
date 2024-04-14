from flask import Blueprint, jsonify, request
from app.model import Image
from app.service import ImageService
from http import HTTPStatus

def get_blueprint(srvc: ImageService) -> Blueprint:
    bp = Blueprint("Image", __name__)
    
    @bp.get('/image')
    def getImage():
        image = srvc.select()
        return jsonify(image)

    @bp.get('/image/<int:id>')
    def getImagebyid(id):
        image = srvc.select(id)
        return jsonify(image)
    
    @bp.post('/image')
    def postImage():
        data = request.json
        image = Image(
           link=data['link'],
           product_id=data['product_id']
        )
        status = srvc.insert(image.load())
        return jsonify(image), HTTPStatus.CREATED if status == 201 else status
    
    return bp
