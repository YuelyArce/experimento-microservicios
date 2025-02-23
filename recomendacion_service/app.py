from confluent_kafka import Consumer
from flask import Flask, request, jsonify
from flask_restful import Api
import threading
from vistas import Recomendaciones, Home

# Configurar el consumidor de Kafka
c = Consumer({'bootstrap.servers': 'localhost:9092', 'group.id': 'python-consumer', 'auto.offset.reset': 'earliest'})
print('Kafka Consumer has been initiated...')
def consume_messages():
    c.subscribe(['ventas-topic'])

    while True:
        msg = c.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            print('Error: {}'.format(msg.error()))
            continue
        data = msg.value().decode('utf-8')
        print(f"Mensaje recibido: {data}")
    c.close()

    
app = Flask(__name__)
app_context = app.app_context()
app_context.push()

api = Api(app)
api.add_resource(Home, '/')
api.add_resource(Recomendaciones, '/recomendar')

if __name__ == "__main__":
    # Iniciar el consumidor en un hilo separado
    consumer_thread = threading.Thread(target=consume_messages)
    consumer_thread.start()

    # Iniciar la aplicación Flask
    app.run(host="0.0.0.0", port=5001, debug=True)
