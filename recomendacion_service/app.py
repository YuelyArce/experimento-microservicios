from flask import Flask, request, jsonify
from kafka import KafkaProducer
import json

app = Flask(__name__)

# Configurar el productor de Kafka
producer = KafkaProducer(
    bootstrap_servers="kafka:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

@app.route('/recomendar', methods=['POST'])
def recomendar():
    data = request.json
    video_id = data.get("video_id")
    
    if not video_id:
        return jsonify({"error": "Falta el video_id"}), 400

    # Generar recomendaciones
    recomendaciones = [f"video_recomendado_{i}" for i in range(1, 4)]
    
    # Enviar a Kafka
    mensaje = {"video_id": video_id, "recomendaciones": recomendaciones}
    producer.send("recomendaciones", mensaje)

    return jsonify(mensaje)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
