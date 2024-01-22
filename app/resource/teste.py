from flask import Blueprint, jsonify, request

def get_blueprint() -> Blueprint:
    bp = Blueprint("Teste", __name__)

    @bp.get('/teste')
    def test():
        testing = {
            'id': 0,
            'name': "teste",
            'obj': {
                'pypy': 128937
            }
        }
        return jsonify(testing)

    @bp.get('/teste/<int:id>')
    def test1(id):
        testing = [
            {
                'ID': 0,
                'name': "teste",
                'obj': {
                    'pypy': 128937
                }
            },
            {
                'ID': 1,
                'name': "teste",
                'obj': {
                    'pypy': 128937
                }
            },
            {
                'ID': 2,
                'name': "teste",
                'obj': {
                    'pypy': 128937
                }
            }
        ]
        return jsonify(testing[id])
    
    return bp
