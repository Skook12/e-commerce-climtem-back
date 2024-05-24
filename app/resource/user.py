import smtplib
import re
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token
from app.service import UserService, AddressService
from app.model import (
    User,
    Address,
    is_valid_phone,
    is_valid_cep,
    is_valid_cpf,
    is_valid_email
)
from http import HTTPStatus


def sendEmail(u: User, config):
    html_body = f"""
        <html>
        <body>
            <h1>Olá {u.name}!</h1>
            <p>Este é um email de validação da sua conta na plataforma Climtem.</p>
        </body>
        </html>
        """
    message = MIMEMultipart()
    message['From'] = config['email']
    message['To'] = u.email
    message['Subject'] = "Confirme a criação da sua conta na Climtem"

    message.attach(MIMEText(html_body, 'html'))
    smtp_server = "smtp.gmail.com"
    port = 587
    try:
        server = smtplib.SMTP(smtp_server, port)
        server.starttls()
        server.login(config['email'], config['p'])
        server.sendmail(config['email'], u.email, message.as_string())
    except Exception as e:
        print(f"Error: {e}")
    finally:
        server.quit()

def get_blueprint(srvc: UserService, addrsrvc: AddressService, config) -> Blueprint:
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
        data = request.json
        adm = False

        try: 
            adm=data['adm']
        except Exception as e:
            print(e)
        
        try:
            u = User(
                name=data['name'],
                email=data['email'],
                password=data['password'],
                cpf=re.sub(r'[^0-9]', '', data['cpf']),
                phone=re.sub(r'[^0-9]', '', data['phone']),
                adm=adm
            )

            a = Address(
                user_id=None,
                number=data['number'],
                complement=data['complement'],
                cep=re.sub(r'[^0-9]', '', data['cep']),
                city=data['city']
            )

            if not is_valid_email(u.email):
                raise ValueError('Email não válido.')
            
            if not is_valid_cpf(u.cpf):
                raise ValueError('CPF não válido.')

            if not is_valid_phone(u.phone):
                raise ValueError('Telefone não válido.')

            if not is_valid_cep(a.cep):
                raise ValueError('CEP não válido.')

            id = srvc.insert(u.load())
            a.user_id = id
            addrsrvc.insert(a.load())

            # sendEmail(u, config)

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
