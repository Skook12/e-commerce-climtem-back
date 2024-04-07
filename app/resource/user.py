from flask import Blueprint, jsonify, request
from app.model import User
from app.service import UserService
from http import HTTPStatus

def get_blueprint(srvc: UserService) -> Blueprint:
    bp = Blueprint("User", __name__)

    @bp.get('/users')
    def getUsers():
        r = srvc.select()
        return jsonify(r)

    @bp.get('/user/<int:id>')
    def getUserbyid(id):
        r = srvc.select(id)
        return jsonify(r)
    
    @bp.post('/users')
    def postUser():
        data = request.json
        r = User(
            name=data['name'],
            email=data['email'],
            password=data['password'],
            phone=data['phone']
        )
        status = srvc.insert(r.load())
        return jsonify(r), HTTPStatus.CREATED if status == 201 else status
    
    return bp
