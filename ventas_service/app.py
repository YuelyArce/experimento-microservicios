from flask import Flask, request, jsonify
from confluent_kafka import Producer
import json


app = Flask(__name__)

# Configurar el productor de Kafka
p = Producer({'bootstrap.servers': 'localhost:9092'})
print('Kafka Producer has been initiated...')

@app.route('/')
def home():
    return "Servicio de ventas en ejecución"

@app.route('/registroVenta', methods=['POST'])
def venta():
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
        "total_venta": cantidad * precio  # Calcular el total de la venta
    }

    message = json.dumps(venta_info).encode('utf-8')  # Convertir el diccionario a JSON y luego a bytes

    # Enviar el mensaje a Kafka
    p.produce('ventas-topic', message)
    p.flush()  # Asegura que se envíen todos los mensajes
    print(f"Mensaje enviado a Kafka: {message}")

    return jsonify(venta_info)  # Retorna el mensaje enviado como respuesta# Retorna el mensaje enviado como respuesta

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
