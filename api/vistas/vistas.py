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

from modelos import db, Usuario, UsuarioSchema, File, FileSchema

file_schema = FileSchema()
usuario_schema = UsuarioSchema()  # Instanciar esquema creado

class VistaHealthCheck(Resource):

    def get(self):
        return "Health check", 200

class VistaSignIn(Resource):
  def post(self):
    nuevo_usuario = Usuario(username=request.form['username'],
                            password=request.form['password'],
                            email=request.form['email'])

    db.session.add(nuevo_usuario)
    db.session.commit()

    return {'mensaje': 'usuario creado exitosamente', 'id': nuevo_usuario.id}


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
    u_username = request.form['username']
    u_password = request.form['password']
    usuario = Usuario.query.filter_by(username=u_username, password = u_password).first()
    if usuario:
      objeto_usuario = usuario_schema.dump(usuario)
      del objeto_usuario['password']
      token_de_acceso = create_access_token(identity=objeto_usuario)
      return {'mensaje':'Inicio de sesión exitoso', "token": token_de_acceso}, 200
    else:
      return {'mensaje':'Nombre de usuario o contraseña incorrectos'}, 401

class VistaFile(Resource):
    def get(self, filename):
      processed_file_formats = ['zip', 'gz', 'bz2']
      filename_parts = filename.split('.')
      if filename_parts[-1] in processed_file_formats:
        PROCESSED_FOLDER = './processed'
        return send_from_directory(PROCESSED_FOLDER, filename)
      else:
        UPLOAD_FOLDER = './uploads'
        return send_from_directory(UPLOAD_FOLDER, filename)

class VistaGetTask(Resource):
    @jwt_required()
    def get(self, task_id):
       file = File.query.get_or_404(task_id)
       return file_schema.dump(file)

    @jwt_required()
    def delete(self, task_id):
      file = File.query.filter_by(id=task_id).first()
      if file:
        db.session.delete(file)
        db.session.commit()
        return {'mensaje': f'Tarea {task_id} eliminada satisfactoriamente'}
      else:
        return {'mensaje': f'Error al eliminar tarea {task_id}'}

