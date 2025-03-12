from flask import request, jsonify, make_response
from flask_restful import Resource
from datetime import datetime
from flask_restful import Resource
from utils.security import validate_token
from modelos.modelos import db, Producto


class validar_token(Resource):

    def post(self):
        
        headers = dict(request.headers)
        if "Token" in headers.keys(): 
            data_token, status_code = validate_token(headers["Token"])
            if status_code == 200:
                print('hola')
                return jsonify({"message": "Token valido", "data": data_token})
            else:
                return make_response(jsonify(data_token), status_code)
        
        else: 
            return make_response(jsonify({"message": "Invalid Token"}), 401)

class ModificarProducto(Resource):

    def put(self, producto_id):
        # Validar el token en los headers
        headers = dict(request.headers)
        if "Token" in headers.keys(): 
            data_token, status_code = validate_token(headers["Token"])
            if status_code != 200:
                return make_response(jsonify(data_token), status_code)
        else: 
            return make_response(jsonify({"message": "Invalid Token"}), 401)

        # Buscar el producto en la base de datos
        producto = Producto.query.get(producto_id)
        if not producto:
            return make_response(jsonify({"message": "Producto no encontrado"}), 404)

        # Obtener los datos del request
        data = request.json

        # Actualizar medio de almacenamiento
        if "tipo_almacenamiento" in data:
            producto.tipo_almacenamiento = data["tipo_almacenamiento"]
        else:
            return make_response(jsonify({"message": "No se proporcionó 'tipo_almacenamiento' para actualizar"}), 400)

        # Guardar cambios en la base de datos
        db.session.commit()

        return jsonify({"message": "Producto actualizado exitosamente"})