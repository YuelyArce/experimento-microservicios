from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields, Schema
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

db = SQLAlchemy()

class Venta(db.Model):
    __tablename__ = 'ventas'
    id = db.Column(db.Integer, primary_key=True)
    producto_id = db.Column(db.String(50), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    precio = db.Column(db.Float, nullable=False)
    total_venta = db.Column(db.Float, nullable=False)

    def __init__(self, producto_id, cantidad, precio):
        self.producto_id = producto_id
        self.cantidad = cantidad
        self.precio = precio
        self.total_venta = cantidad * precio

    def __repr__(self):
        return f"<Venta {self.producto_id}>"

class VentaSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Venta
        load_instance = True
