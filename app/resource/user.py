from flask import Blueprint, jsonify, request
from app.model import User
from app.service import UserService
from http import HTTPStatus

def get_blueprint(srvc: UserService) -> Blueprint:
    bp = Blueprint("User", __name__)

    @bp.get('/users')
    def getUsers():
        users = srvc.select()
        return jsonify(users)

    @bp.get('/user/<int:id>')
    def getUserbyid(id):
        user = srvc.select(id)
        return jsonify(user)
    
    @bp.post('/users')
    def postUser():
        data = request.json
        user = User(
            name=data['name'],
            email=data['email'],
            password=data['password'],
            phone=data['phone']
        )
        status = srvc.insert(user.load())
        return jsonify(user), HTTPStatus.CREATED if status == 201 else status
    
    return bp
