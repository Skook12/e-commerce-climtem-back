import re
from flask import Blueprint, jsonify, request
from app.utils.mail import sendEmail
from flask_jwt_extended import create_access_token
from app.service import UserService, AddressService
from app.security.jwt_utils import token_required
from app.model import (
    User,
    Address,
    is_valid_phone,
    is_valid_cep,
    is_valid_cpf,
    is_valid_email
)
from http import HTTPStatus


def get_blueprint(srvc: UserService, addrsrvc: AddressService) -> Blueprint:
    bp = Blueprint("User", __name__)

    @bp.get('/users/<int:id>')
    @token_required
    def getUserbyid(id):
        r = srvc.select(f'u JOIN User_Address a ON a.ID_User = u.ID_User WHERE u.ID_User = {id}')
        return jsonify(r)

    @bp.put('/users/<int:id>')
    @token_required
    def changeUserInfo(id):
        '''Route for change user info'''
        data = request.json
        r = {
            "name": data['name'],
            "email": data['email'],
            "phone": re.sub(r'[^0-9]', '', data['phone'])
        }
     
        a = {
            "num": data['num'],
            "complement": data['complement'],
            "cep": re.sub(r'[^0-9]', '', data['cep']),
            "city": data['city']
        }

        if not is_valid_email(r.email):
            raise 'Email não válido.'

        if not is_valid_phone(r.phone):
            raise 'Telefone não válido.'

        if not is_valid_cep(a.cep):
            raise 'CEP não válido.'

        for attr, val in r.items():
            srvc.update(attr, f'ID_User = {id}', val)

        for attr, val in a.items():
            addrsrvc.update(attr, f'ID_User = {id}', val)
        
        return jsonify({'msg': f'{r["name"]} Atualizou suas informações.'})

    @bp.post('/users/signup')
    def SignUp():
        '''Route for signUp user'''
        data = request.json

        try:
            u = User(
                name=data['name'],
                email=data['email'],
                password=data['password'],
                cpf=re.sub(r'[^0-9]', '', data['cpf']),
                phone=re.sub(r'[^0-9]', '', data['phone']),
                adm=False
            )

            a = Address(
                user_id=None,
                num=data['number'],
                complement=data['complement'],
                cep=re.sub(r'[^0-9]', '', data['cep']),
                city=data['city']
            )

            if not is_valid_email(u.email):
                raise 'Email não válido.'
            
            if not is_valid_cpf(u.cpf):
                raise 'CPF não válido.'

            if not is_valid_phone(u.phone):
                raise 'Telefone não válido.'

            if not is_valid_cep(a.cep):
                raise 'CEP não válido.'

            id = srvc.insert(u.load())
            a.user_id = id
            addrsrvc.insert(a.load())

            # sendEmail(u, f"""
            #     <html>
            #         <body>
            #             <h1>Olá {u.name}!</h1>
            #             <p>Este é um email de validação da sua conta na plataforma Climtem.</p>
            #         </body>
            #     </html>
            # """, config)

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
