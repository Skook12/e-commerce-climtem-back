import jwt
from app.model import User
from app.service import UserService
from http import HTTPStatus
from flask import Blueprint, jsonify, request

def get_blueprint(srvc: UserService, config) -> Blueprint:
    bp = Blueprint("User", __name__)

    @bp.get('/users')
    def getUsers():
        r = srvc.select()
        return jsonify(r)

    @bp.get('/user/<int:id>')
    def getUserbyid(id):
        r = srvc.select(f'WHERE ID_User = {id}')
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

    @bp.post('/users/login')
    def Login():
        data = request.json

        if not data["email"] or not data["pass"]:
            return jsonify({"message": "Usuário e senha são obrigatórios"}), HTTPStatus.BAD_REQUEST

        r = srvc.select(f'u WHERE u.email = \'{data["email"]}\' and u.password = \'{data["pass"]}\'')
        if r != None:
            token_payload = {
                "id": r[0]['id'],
                "username": r[0]['name'],
                "email": r[0]['email'],
                "phone": r[0]['phone']
            }
            token = jwt.encode(token_payload, config['SKey'], algorithm="HS256")

            return jsonify({"token": token}), HTTPStatus.ACCEPTED
        else:
            return jsonify({"message": "Usuário ou Senha inválidos."}), HTTPStatus.UNAUTHORIZED

    return bp
