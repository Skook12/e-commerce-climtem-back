from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt
from http import HTTPStatus
from functools import wraps

def admin_required(fn):
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        claims = get_jwt()
        if not claims.get('adm', False):
            return jsonify({"msg": "Admins only!"}), HTTPStatus.FORBIDDEN
        return fn(*args, **kwargs)
    return wrapper
