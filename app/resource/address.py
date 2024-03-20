from flask import Blueprint, jsonify, request
from app.model import Address
from app.service import AddressService
from http import HTTPStatus

def get_blueprint(srvc: AddressService) -> Blueprint:
    bp = Blueprint("Address", __name__)
    
    @bp.get('/address')
    def getAddress():
        '''[To be excluded] Development only!'''
        address = srvc.select()
        return jsonify(address)

    @bp.get('/address/<int:id>')
    def getAddressbyid(id):
        address = srvc.select(id)
        return jsonify(address)
    
    @bp.post('/address')
    def postAddress():
        data = request.json
        address = Address(
            user_id=data['user_id'],
            number=data['number'],
            complement=data['complement'],
            cep=data['cep'],
            city=data['city']
        )
        status = srvc.insert(address.load())
        return jsonify(address), HTTPStatus.CREATED if status == 201 else status
    
    return bp
