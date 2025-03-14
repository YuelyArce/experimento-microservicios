from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields, Schema
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

db = SQLAlchemy()

class BlackList(db.Model):
    __tablename__ = 'black_list'
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(50), nullable=False)
  

class BlackListSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = BlackList
        load_instance = True