import requests
from flask import request, jsonify, make_response
from flask_restful import Resource
from utils.security import validate_token
from modelos.modelos import db, Producto

AUDITORIA_URL = "http://localhost:5004/evento"

class validar_token(Resource):
    def post(self):
        headers = dict(request.headers)
        if "Token" not in headers:
            return make_response(jsonify({"message": "Invalid Token"}), 401)

        data_token, status_code = validate_token(headers["Token"])
        if status_code == 200:
            usuario = data_token.get("usuario")
            requests.post(AUDITORIA_URL, json={
                "usuario": usuario,
                "estado": "validación de token exitosa",
                "detalles": "Token válido"
            })
            return jsonify({"message": "Token válido", "data": data_token})

        return make_response(jsonify(data_token), status_code)

class ModificarProducto(Resource):
    def put(self, producto_id):
        # Validar token
        headers = dict(request.headers)
        if "Token" not in headers:
            return make_response(jsonify({"message": "Invalid Token"}), 401)

        data_token, status_code = validate_token(headers["Token"])
        if status_code != 200:
            return make_response(jsonify(data_token), status_code)
        usuario = data_token.get("usuario", "Desconocido")

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

        # Guardar cambios y auditar
        try:
            db.session.commit()
            requests.post(AUDITORIA_URL, json={
                "usuario": usuario,
                "estado": "modificación exitosa",
                "detalles": f"Producto ID {producto_id} actualizado de '{old_value}' a '{new_value}'"
            })
            return jsonify({"message": "Producto actualizado exitosamente"})
        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({"message": "Error actualizando el producto", "error": str(e)}), 500)