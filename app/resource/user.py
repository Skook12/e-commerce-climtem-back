from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token
from app.model import User, Address
from app.service import UserService, AddressService
from http import HTTPStatus

def get_blueprint(srvc: UserService, addrsrvc: AddressService) -> Blueprint:
    bp = Blueprint("User", __name__)

    @bp.get('/users')
    def getUsers():
        #TODO: REMOVE route
        """Development only"""
        r = srvc.select()
        return jsonify(r)

    @bp.get('/user/<int:id>')
    def getUserbyid(id):
        #TODO: REMOVE route
        r = srvc.select(f'WHERE ID_User = {id}')
        return jsonify(r)
    
    @bp.post('/users/signup')
    def SignUp():
        '''Route for signUp user'''
        try:
            data = request.json
            u = User(
                name=data['name'],
                email=data['email'],
                password=data['password'],
                cpf=data['cpf'],
                phone=data['phone'],
                adm=data['adm']
            )
            id = srvc.insert(u.load())
            a = Address(
                user_id=id,
                number=data['number'],
                complement=data['complement'],
                cep=data['cep'],
                city=data['city']
            )
            addrsrvc.insert(a.load())
            #TODO: Send email to new user to verify account creation
        except Exception as e:
            return jsonify({"[ERROR]": str(e)}), HTTPStatus.BAD_REQUEST
        return jsonify([u, a]), HTTPStatus.CREATED

    @bp.post('/users/login')
    def Login():
        '''Route for Login user'''
        data = request.json

        if not data["email"] or not data["pass"]:
            return jsonify({"message": "Usuário e senha são obrigatórios"}), HTTPStatus.BAD_REQUEST

        r = srvc.select(f'u WHERE u.email = \'{data["email"]}\' and u.password = \'{data["pass"]}\'')
        if r != None:
            payload = {
                "id": r[0]['id'],
                "email": r[0]['email'],
                "adm": r[0]['adm']
            }
            access_token = create_access_token(identity=payload['email'], additional_claims={"adm": payload['adm'], "id": payload['id']})

            return jsonify({"access_token": access_token}), HTTPStatus.ACCEPTED
        else:
            return jsonify({"message": "Usuário ou Senha inválidos."}), HTTPStatus.UNAUTHORIZED

    return bp
