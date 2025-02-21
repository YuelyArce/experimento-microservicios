from flask import Flask, request, jsonify
from confluent_kafka import Producer
import json
import time

app = Flask(__name__)

# Configurar el productor de Kafka
p = Producer({'bootstrap.servers': 'localhost:9092'})
print('Kafka Producer has been initiated...')

@app.route('/')
def home():
    return "Servicio de Recomendaciones en ejecución"

@app.route('/recomendar', methods=['POST'])
def recomendar():
    data = request.json
    video_id = data.get("video_id")

    if not video_id:
        return jsonify({"error": "Falta el video_id"}), 400

    # Generar recomendaciones
    recomendaciones = [f"video_recomendado_{i}" for i in range(1, 4)]

    # Crear el mensaje para Kafka (convertir a JSON)
    m = {"video_id": video_id, "recomendaciones": recomendaciones}
    message = json.dumps(m).encode('utf-8')  # Convertir el diccionario a JSON y luego a bytes

    # Enviar el mensaje a Kafka
    p.produce('user-tracker', message)
    p.flush()  # Asegura que se envíen todos los mensajes
    print(f"Mensaje enviado a Kafka: {message}")

    return jsonify(m)  # Retorna el mensaje enviado como respuesta

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
