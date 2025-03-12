from flask import request, jsonify, make_response
from flask_restful import Resource
from datetime import datetime
from flask_restful import Resource
from utils.security import write_token

usuarios_quemados = {
    'omar': {'password': 'admin', 'role': 'ademin'},
    'adriana': {'password': '1234', 'role': 'vendedor'},
    'alejandra': {'password': '1234', 'role': 'tendero'},
    'sebastian': {'password': '1234', 'role': 'logistica'},
    }

class Home(Resource):

    def get(self):
        return "Servicio de login en ejecución"

class Login(Resource):

    def post(self):
        try:
            data = request.json
            usuario = data['usuario']
            password =  data['password']
            if usuario in usuarios_quemados.keys() and usuarios_quemados[usuario]['password'] == password:
                data['role'] = usuarios_quemados[usuario]['role']
                token = write_token(data)
                return jsonify({"token": token})
            else:
                return make_response(jsonify({'message': 'usuario o contraseña incorrecta'}), 200)
        except KeyError:
            return make_response(jsonify({'message': 'Datos de request erroneos'}), 422)
 

        