from flask import Flask, request, jsonify
from flask_restful import Api
from vistas.vistas import Login, Home
import json


# Configuración de la aplicación Flask
app = Flask(__name__)


api = Api(app)
api.add_resource(Home, '/')
api.add_resource(Login, '/login')

if __name__ == "__main__":
    # Iniciar el consumidor en un hilo separado

    # Iniciar la aplicación Flask
    app.run(host="0.0.0.0", port=5001, debug=True)
