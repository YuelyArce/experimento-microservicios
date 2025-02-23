from confluent_kafka import Consumer
from flask import Flask, request, jsonify
from flask_restful import Api
import threading
from vistas import Recomendaciones, Home
from modelos import db, Venta
import json

# Configurar el consumidor de Kafka
c = Consumer({'bootstrap.servers': 'localhost:9092', 'group.id': 'python-consumer', 'auto.offset.reset': 'earliest'})
print('Kafka Consumer has been initiated...')

# Función para consumir mensajes
def consume_messages():
    c.subscribe(['ventas-topic'])  # Suscripción al tema de Kafka

    while True:
        msg = c.poll(1.0)  # Tiempo de espera de 1 segundo
        if msg is None:
            continue
        if msg.error():
            print(f'Error: {msg.error()}')
            continue

        data = msg.value().decode('utf-8')  # Decodificar el mensaje en formato JSON
        print(f"Mensaje recibido: {data}")

        # Convertir el mensaje de JSON a un diccionario
        mensaje = json.loads(data)

        # Iniciar el contexto de aplicación para este hilo
        with app.app_context():
            # Crear un nuevo registro en la base de datos
            nueva_venta = Venta(
                producto_id=mensaje['producto_id'],
                cantidad=mensaje['cantidad'],
                precio=mensaje['precio'],
                total_venta=mensaje['total_venta']
            )

            # Agregar el objeto Venta a la base de datos y confirmar la transacción
            db.session.add(nueva_venta)
            db.session.commit()
            print("Venta guardada en la base de datos")

    c.close()

# Configuración de la aplicación Flask
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///entrenamiento.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()

api = Api(app)
api.add_resource(Home, '/')
api.add_resource(Recomendaciones, '/recomendar')

if __name__ == "__main__":
    # Iniciar el consumidor en un hilo separado
    consumer_thread = threading.Thread(target=consume_messages)
    consumer_thread.start()

    # Iniciar la aplicación Flask
    app.run(host="0.0.0.0", port=5001, debug=True)
