import re
from flask import Blueprint, jsonify, request, url_for, render_template
from app.utils.mail import sendEmail
from flask_jwt_extended import create_access_token, get_jwt
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
        data = dict(request.json)
        r = {
            "name": data.get('name'),
            "email": data.get('email'),
            "phone": re.sub(r'[^0-9]', '', data.get('phone'))
        }
     
        a = {
            "num": data.get('num'),
            "complement": data.get('complement'),
            "cep": re.sub(r'[^0-9]', '', data.get('cep')),
            "city": data.get('city')
        }

        if not is_valid_email(r['email']):
            raise 'Email não válido.'

        if not is_valid_phone(r['phone']):
            raise 'Telefone não válido.'

        if not is_valid_cep(a['cep']):
            raise 'CEP não válido.'

        for attr, val in r.items():
            if val is not None:
                srvc.update(attr, f'ID_User = {id}', val)

        for attr, val in a.items():
            if val is not None:
                addrsrvc.update(attr, f'ID_User = {id}', val)
        
        return jsonify({'msg': f'{r["name"]} Atualizou suas informações.'})

    @bp.post('/users/forgetpassword/<string:email>')
    def forgetpassword(email):
        r = srvc.select(f'u WHERE u.email = \'{email}\'')
        if r == None:
            return jsonify({'msg': "Email não encontrado."}), HTTPStatus.NOT_FOUND
        
        payload = {
            "id": r[0]['id'],
            "email": r[0]['email'],
        }

        access_token = create_access_token(identity=payload['email'], additional_claims={"id": payload['id']})
        link = url_for('User.validateuserToken', token=access_token, _external=True)

        sendEmail(email, f"""
            <html>
                <body>
                    <h1>Olá {r[0]['name']}!</h1>
                    <p>Faça a redefinição da sua senha através do link abaixo.</p>
                    <a href={link}>
                        Redefinir senha.
                    </a>
                </body>
            </html>
        """, "Redefinição de senha.")

        return jsonify({'msg': 'Email de redefinição enviado.'}), HTTPStatus.ACCEPTED

    @bp.get('/users/<string:token>')
    def validateuserToken(token):
        if token:
            return render_template('validate.html', access_token=token)
        else:
            return jsonify({'message': 'Token inválido ou expirado.'}), HTTPStatus.BAD_REQUEST

    @bp.put('/users/passwordreset/<int:id>')
    @token_required
    def passwordreset(id):
        data = request.json
        claims = get_jwt()
        srvc.update('password', f'ID_User = {id}', data['password'])
        sendEmail(claims.get('email'), f"""
            <html>
                <body>
                    <h1>Olá {claims.get('email')}!</h1>
                    <p>Sua senha foi redefinida com sucesso!</p>
                </body>
            </html>
        """, "Senha alterada.")
        return jsonify({'msg': 'Senha alterada com sucesso.'}), HTTPStatus.ACCEPTED

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

        except Exception as e:
            return jsonify({"[ERROR]": str(e)}), HTTPStatus.BAD_REQUEST
        sendEmail(u.email, f"""
                <html>
                    <body>
                        <h1>Olá {u.name}!</h1>
                        <p>Este é um email de validação da sua conta na plataforma Climtem.</p>
                    </body>
                </html>
        """)

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
