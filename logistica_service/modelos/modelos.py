from flask_sqlalchemy import SQLAlchemy


# Crear la instancia de SQLAlchemy
db = SQLAlchemy()

# Definir modelo de Producto
class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    nombre_productor = db.Column(db.String(100), nullable=False)
    fecha_compra = db.Column(db.Date, nullable=False)
    tipo_almacenamiento = db.Column(db.String(50), nullable=False)
    fecha_salida = db.Column(db.Date, nullable=True)
    ubicacion = db.Column(db.String(200), nullable=False)

