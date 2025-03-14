from flask import Flask, request, jsonify
from flask_restful import Api
from vistas.vistas import Usuarios, Usuario
from modelos.modelos import db
import json


# Configuración de la aplicación Flask
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///black.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

app_context = app.app_context()
app_context.push()


api = Api(app)
api.add_resource(Usuario, '/black/<int:id_usuario>')
api.add_resource(Usuarios, '/black')


with app.app_context():
    db.create_all()

if __name__ == "__main__":
    # Iniciar la aplicación Flask
    app.run(host="0.0.0.0", port=3001, debug=True)
