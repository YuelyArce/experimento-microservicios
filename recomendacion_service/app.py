from confluent_kafka import Consumer
from flask import Flask
import threading

app = Flask(__name__)

# Configurar el consumidor de Kafka
c = Consumer({'bootstrap.servers': 'localhost:9092', 'group.id': 'python-consumer', 'auto.offset.reset': 'earliest'})
print('Kafka Consumer has been initiated...')

@app.route("/")
def home():
    return "Servicio de Recomendaciones en ejecución"

def consume_messages():
    c.subscribe(['user-tracker'])

    while True:
        msg = c.poll(1.0)  # Timeout de 1 segundo
        if msg is None:
            continue
        if msg.error():
            print('Error: {}'.format(msg.error()))
            continue
        data = msg.value().decode('utf-8')
        print(f"Mensaje recibido: {data}")
    c.close()

if __name__ == "__main__":
    # Iniciar el consumidor en un hilo separado
    consumer_thread = threading.Thread(target=consume_messages)
    consumer_thread.start()

    # Iniciar la aplicación Flask
    app.run(host="0.0.0.0", port=5001, debug=True)
