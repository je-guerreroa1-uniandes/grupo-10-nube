# ZIP, 7Z, TAR.GZ, TAR.BZ2
from modelos import db, Usuario, UsuarioSchema
import zipfile
import tarfile

import os
from enum import Enum

from _curses import flash
from flask import request
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from flask import url_for
from flask import send_from_directory
from flask_restful import Resource
from werkzeug.utils import secure_filename
# from sqlalchemy.exc import IntegrityError
# from sqlalchemy import and_
# from datetime import datetime
import hashlib

from modelos import db, Usuario, UsuarioSchema

usuario_schema = UsuarioSchema()

class VistaHealthCheck(Resource):

    def get(self):
        return "Health check", 200

class VistaSignIn(Resource):
  def post(self):
    nuevo_usuario = Usuario(username=request.json['username'],
                            password=request.json['password'],
                            email=request.json['email'])

    token_de_acceso = create_access_token(identity=request.json['username'])

    db.session.add(nuevo_usuario)
    db.session.commit()

    return {'mensaje': 'usuario creado exitosamente', 'token_de_acceso': token_de_acceso}


  @jwt_required()
  def get(self):
    return [usuario_schema.dump(usuario) for usuario in Usuario.query.all()]



class VistaUpdateSignIn(Resource):
  @jwt_required()
  def get(self, id_usuario):
    return usuario_schema.dump(Usuario.query.get_or_404(id_usuario))

  @jwt_required()
  def put(self, id_usuario):
    usuario = Usuario.query.get_or_404(id_usuario)
    usuario.username = request.json.get('username', usuario.username)
    usuario.password = request.json.get('password', usuario.password)
    usuario.email = request.json.get('email', usuario.email)
    db.session.commit()  # Guarda cambios
    return usuario_schema.dump(usuario)

  @jwt_required()
  def delete(self, id_usuario):
    usuario = Usuario.query.get_or_404(id_usuario)
    db.session.delete(usuario)
    db.session.commit()
    return 'Usuario eliminado exitosamente', 204




class VistaLogIn(Resource):
  def post(self):
    u_username = request.json['username']
    u_password = request.json['password']
    usuario = Usuario.query.filter_by(username=u_username, password = u_password).all()
    if usuario:
      return {'mensaje':'Inicio de sesión exitoso'}, 200
    else:
      return {'mensaje':'Nombre de usuario o contraseña incorrectos'}, 401
