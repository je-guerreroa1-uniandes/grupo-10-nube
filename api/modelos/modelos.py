from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields, Schema
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

db = SQLAlchemy()


class Usuario(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(50))
  password = db.Column(db.String(50))
  email = db.Column(db.String(128))


class UsuarioSchema(SQLAlchemyAutoSchema):
  class Meta:
    model = Usuario
    include_relationships = True
    load_instance = True
