import requests
from flask import request, jsonify, make_response
from flask_restful import Resource
from utils.security import validate_token
from modelos.modelos import db, Producto
from os import getenv

AUDITORIA_URL = "http://localhost:5004/evento"
BLACK_URL =  "http://127.0.0.1:3001/black"

class validar_token(Resource):
    def post(self):
        headers = dict(request.headers)
        if "Token" not in headers:
            return make_response(jsonify({"message": "Invalid Token"}), 401)

        data_token, status_code = validate_token(headers["Token"])
        if status_code == 200:
            usuario = data_token.get("usuario")
            rol = data_token.get("role")
            requests.post(AUDITORIA_URL, json={
                "usuario": usuario,
                "rol": rol,
                "estado": "validación de token exitosa",
                "detalles": "Token válido"
            })
            return jsonify({"message": "Token válido", "data": data_token})

        return make_response(jsonify(data_token), status_code)

class ModificarProducto(Resource):
    def put(self, producto_id):
        headers = dict(request.headers)

        # Validar que el token está presente
        if "Token" not in headers:
            return make_response(jsonify({"message": "Invalid Token"}), 401)

        # Validar token
        data_token, status_code = validate_token(headers["Token"])
        if status_code != 200:
            return make_response(jsonify(data_token), status_code)

        # Extraer usuario del token validado
        usuario = data_token.get("usuario", "Desconocido")
        rol = data_token.get("role")

        # Verificar si el usuario está en la lista negra
        header = {'TOKEN': getenv('TOKEN_BLACK')}
        try:
            response = requests.get(BLACK_URL, json={'usuario': usuario}, headers=header)
            response.raise_for_status()
            usuario_in_black = response.json().get('black', False)
        except requests.RequestException as e:
            return make_response(jsonify({"message": "Error consultando lista negra", "error": str(e)}), 500)

        # Si el usuario está en la lista negra, bloquearlo
        if usuario_in_black:
            return make_response(jsonify({"message": "Usuario bloqueado, no tiene permisos"}), 403)


        # Buscar el producto en la base de datos
        producto = Producto.query.get(producto_id)
        if not producto:
            return make_response(jsonify({"message": "Producto no encontrado"}), 404)

        # Validar datos del request
        data = request.json
        if "tipo_almacenamiento" not in data:
            return make_response(jsonify({"message": "No se proporcionó 'tipo_almacenamiento' para actualizar"}), 400)

        old_value = producto.tipo_almacenamiento
        new_value = data["tipo_almacenamiento"]
        producto.tipo_almacenamiento = new_value


        try:
            db.session.commit()
            requests.post(AUDITORIA_URL, json={
                "usuario": usuario,
                "estado": "modificación exitosa",
                "rol": rol,
                "detalles": f"Producto ID {producto_id} actualizado de '{old_value}' a '{new_value}'"
            })
            return jsonify({"message": "Producto actualizado exitosamente"})
        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({"message": "Error actualizando el producto", "error": str(e)}), 500)