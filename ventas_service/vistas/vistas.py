from flask import request, jsonify
from flask_jwt_extended import jwt_required, create_access_token
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from flask_restful import Resource
import json
from confluent_kafka import Producer
from modelos import db, Venta

# Configurar el productor de Kafka
p = Producer({'bootstrap.servers': 'localhost:9092'})
print('Kafka Producer has been initiated...')

class Home(Resource):

    def get(self):
        return "Servicio de ventas en ejecución"


class Ventas(Resource):

    def post(self):

        # Obtener los datos del cuerpo de la solicitud
        data = request.json
        producto_id = data.get("producto_id")
        cantidad = data.get("cantidad")
        precio = data.get("precio")

        if not producto_id or not cantidad or not precio:
            return jsonify({"error": "Faltan datos en la venta"}), 400

        # Crear el mensaje para Kafka (convertir a JSON)
        venta_info = {
            "producto_id": producto_id,
            "cantidad": cantidad,
            "precio": precio,
            "total_venta": cantidad * precio
        }

        message = json.dumps(venta_info).encode('utf-8')
        # Enviar el mensaje a Kafka
        p.produce('ventas-topic', message)
        p.flush()
        print(f"Mensaje enviado a Kafka: {message}")

        # Guardar la venta en la base de datos
        nueva_venta = Venta(producto_id=producto_id, cantidad=cantidad, precio=precio)
        db.session.add(nueva_venta)
        db.session.commit()

        return jsonify(venta_info)