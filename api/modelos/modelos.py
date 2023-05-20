from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields, Schema
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

db = SQLAlchemy()

class Usuario(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(50))
  password = db.Column(db.String(50))
  email = db.Column(db.String(128))

class File(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  filename = db.Column(db.String(250))
  to_extension = db.Column(db.String(128))
  processed_filename = db.Column(db.String(250))
  state = db.Column(db.String(20))
  user_id = db.Column(db.Integer)
  created_at = db.Column(db.String(128))
  updated_at = db.Column(db.String(128))

class UsuarioSchema(SQLAlchemyAutoSchema):
  class Meta:
    model = Usuario
    include_relationships = True
    load_instance = True

class FileSchema(SQLAlchemyAutoSchema):
  class Meta:
    model = File
    include_relationships = True
    load_instance = True
