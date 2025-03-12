from flask import request, jsonify, make_response
from flask_restful import Resource
from datetime import datetime
from flask_restful import Resource
from utils.security import validate_token


class Logistica(Resource):

    def post(self):
        
        headers = dict(request.headers)
        if "Token" in headers.keys(): 
            data_token, status_code = validate_token(headers["Token"])
            if status_code == 200:
                pass
            else:
                return make_response(jsonify(data_token), status_code)
        
        else: 
            return make_response(jsonify({"message": "Invalid Token"}), 401)


        


       