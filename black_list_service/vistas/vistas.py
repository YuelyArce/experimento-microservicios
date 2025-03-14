import requests
from flask import request, jsonify, make_response
from flask_restful import Resource
from datetime import datetime
from flask_restful import Resource
from utils.security import validate_token
from modelos.modelos import BlackList, db



class Usuarios(Resource):

    def post(self):
        
        headers = dict(request.headers)
        if "Token" not in headers:
            return make_response(jsonify({"message": "Invalid Token"}), 401)
        
        data_token, status_code = validate_token(headers["Token"])
        if status_code == 200 and data_token['role'] == 'admin':
            data = request.json
            usuario = data['usuario']
            new_usuario_black = BlackList(usuario=usuario)
            db.session.add(new_usuario_black)
            db.session.commit()
            return {"mensaje": "usuario agregado con exito"}
        
    def get(self):

        headers = dict(request.headers)
        if "Token" not in headers:
            return make_response(jsonify({"message": "Invalid Token"}), 401)
        
        data_token, status_code = validate_token(headers["Token"])
        if status_code == 200 and data_token['role'] == 'admin':
            data = request.json
            usuario = data['usuario']
            usuario = BlackList.query.filter(BlackList.usuario == usuario).first()
            if usuario is None:
                return {'mensaje': "usuario no esta en black list", 'black': False}
            else:
                return {'mensaje': "usuario esta en black", 'black': True, 'id': usuario.id}


class Usuario(Resource):
    def delete(self, id_usuario):
        headers = dict(request.headers)
        if "Token" not in headers:
            return make_response(jsonify({"message": "Invalid Token"}), 401)
        
        data_token, status_code = validate_token(headers["Token"])
        if status_code == 200 and data_token['role'] == 'admin':
            borrado = BlackList.query.get_or_404(id_usuario)
            db.session.delete(borrado)
            db.session.commit()
            return '', 204


