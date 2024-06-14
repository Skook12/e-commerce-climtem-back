import os
import base64
from flask import Blueprint, jsonify, request
from app.security.jwt_utils import admin_required
from app.service import StorageService

def get_blueprint(srvc: StorageService) -> Blueprint:
    bp = Blueprint("Image", __name__)
    
    @bp.get('/images')
    def getImage():
        image = srvc.select()
        return jsonify(image)

    @bp.get('/products/images/<int:product_id>')
    def getImagebyid(product_id):
        image = srvc.select(product_id)
        return jsonify(image)

    @bp.get('/banners')
    def getBanners():
        f = []
        for i, filename in enumerate(os.listdir('/app/app/content/banners')):
            file_path = os.path.join('/app/app/content/banners', filename)
            if os.path.isfile(file_path):
                with open(file_path, "rb") as file:
                    banner_data = base64.b64encode(file.read()).decode('utf-8')
                    f.append({'id': i, 'banner': banner_data, 'name': filename})
        return jsonify(f)

    @bp.delete('/banners/<string:name>')
    @admin_required
    def deleteBanner(name):
        folder_path = '/app/app/content/banners'
        file_path = os.path.join(folder_path, name)
        code = 404
        if os.path.exists(file_path):
            os.remove(file_path)
            code = 200

        return jsonify(code)

    @bp.post('/banners')
    @admin_required
    def postBanners():
        file = request.files['file']
        st = srvc.loadFile(file, 'banners/')
        return jsonify(st)

    return bp
