from flask import Flask, request, jsonify
from confluent_kafka import Producer
from flask_restful import Api
from vistas import Home, Ventas
import json



app = Flask(__name__)
app_context = app.app_context()
app_context.push()

api = Api(app)
api.add_resource(Home, '/')
api.add_resource(Ventas, '/registroVenta')

# Configurar el productor de Kafka
p = Producer({'bootstrap.servers': 'localhost:9092'})
print('Kafka Producer has been initiated...')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
