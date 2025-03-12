from flask import Flask, request, jsonify
from flask_restful import Api
from modelos.modelos import db, Producto
from datetime import datetime
from vistas.vistas import Logistica
import json


# Configuración de la aplicación Flask
app = Flask(__name__)

# Configurar SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///productos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar la base de datos con la aplicación
db.init_app(app)

# Crear las tablas  y agregar datos iniciales
with app.app_context():
    db.create_all()

    # Verificar si ya hay datos para no duplicarlos
    if Producto.query.first() is None:
        productos_iniciales = [
            Producto(
                nombre="Caja Papel",
                nombre_productor="El Bosque",
                fecha_compra=datetime(2025, 3, 1).date(),
                tipo_almacenamiento="Seco",
                fecha_salida=datetime(2025, 3, 10).date(),
                ubicacion="Bodega A1"
            ),
            Producto(
                nombre="Caja esferos",
                nombre_productor="Mundial",
                fecha_compra=datetime(2025, 3, 2).date(),
                tipo_almacenamiento="Seco",
                fecha_salida=datetime(2025, 3, 12).date(),
                ubicacion="Estantería B3"
            ),
            Producto(
                nombre="Marcadores",
                nombre_productor="Super Color",
                fecha_compra=datetime(2025, 3, 3).date(),
                tipo_almacenamiento="Refrigerado",
                fecha_salida=datetime(2025, 3, 8).date(),
                ubicacion="Cámara C5"
            )
        ]

        db.session.add_all(productos_iniciales)
        db.session.commit()

api = Api(app)
api.add_resource(Logistica, '/logistica')

if __name__ == "__main__":
    # Iniciar el consumidor en un hilo separado

    # Iniciar la aplicación Flask
    app.run(host="0.0.0.0", port=4001, debug=True)