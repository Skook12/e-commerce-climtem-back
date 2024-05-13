from flask import Blueprint, jsonify
from app.service import AddressService

def get_blueprint(srvc: AddressService) -> Blueprint:
    bp = Blueprint("Address", __name__)
    
    @bp.get('/address/<int:userid>')
    def getAddressbyUser(userid):
        r = srvc.select(f'ID_User = {userid}')
        return jsonify(r)

    return bp
