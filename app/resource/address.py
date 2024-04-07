from flask import Blueprint, jsonify, request
from app.model import Address
from app.service import AddressService
from http import HTTPStatus

def get_blueprint(srvc: AddressService) -> Blueprint:
    bp = Blueprint("Address", __name__)
    
    @bp.get('/address')
    def getAddress():
        '''[To be excluded] Development only!'''
        r = srvc.select()
        return jsonify(r)

    @bp.get('/address/<int:id>')
    def getAddressbyid(id):
        r = srvc.select(id)
        return jsonify(r)
    
    @bp.post('/address')
    def postAddress():
        data = request.json
        r = Address(
            user_id=data['user_id'],
            number=data['number'],
            complement=data['complement'],
            cep=data['cep'],
            city=data['city']
        )
        status = srvc.insert(r.load())
        return jsonify(r), HTTPStatus.CREATED if status == 201 else status
    
    return bp
