import requests
from os import getenv
from flask import request, jsonify, make_response
from flask_restful import Resource
from datetime import datetime
from flask_restful import Resource
from utils.security import write_token

AUDITORIA_URL = "http://localhost:5004/evento"
BLACK_URL =  "http://127.0.0.1:3001/black"

usuarios_quemados = {
    'omar': {'password': 'admin', 'role': 'admin'},
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
            
            header = {'TOKEN': getenv('TOKEN_BLACK')}
            usuario_black = requests.get(
                BLACK_URL, 
                json={'usuario': usuario}, 
                headers=header
                )
            usuario_in_black = usuario_black.json()['black']
            if usuario in usuarios_quemados.keys() and usuarios_quemados[usuario]['password'] == password and not usuario_in_black:
                data['role'] = usuarios_quemados[usuario]['role']
                token = write_token(data)

                requests.post(AUDITORIA_URL, json={
                    "usuario": usuario,
                    "estado": "login exitoso",
                    "detalles": f"Rol: {data['role']}"
                })

                return jsonify({"token": token})
            else:
                requests.post(AUDITORIA_URL, json={
                    "usuario": usuario,
                    "estado": "login fallido",
                    "detalles": "Usuario o contraseña incorrectos"
                })
                return make_response(jsonify({'message': 'usuario o contraseña incorrecta'}), 200)
        except KeyError:
            return make_response(jsonify({'message': 'Datos de request erroneos'}), 422)
 

        