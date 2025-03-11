from flask import request, jsonify
from flask_restful import Resource
from datetime import datetime
from flask_restful import Resource
from utils.security import write_token

class Home(Resource):

    def get(self):
        return "Servicio de login en ejecución"

class Login(Resource):

    def post(self):

        data = request.json
        token = write_token(data)


        return jsonify({"token": token})