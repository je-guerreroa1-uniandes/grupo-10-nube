# ZIP, 7Z, TAR.GZ, TAR.BZ2
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

class Format(Enum):
    ZIP = 'zip'

class VistaSignIn(Resource):

    def post(self):
        # entrenador = Entrenador.query.filter(
        #     Entrenador.usuario == request.json["usuario"]).first()
        # if entrenador is None:
        #     contrasena_encriptada = hashlib.md5(
        #         request.json["contrasena"].encode('utf-8')).hexdigest()
        #     nuevo_entrenador = Entrenador(
        #         usuario=request.json["usuario"], contrasena=contrasena_encriptada, rol=Rol.ENTRENADOR)
        #     db.session.add(nuevo_entrenador)
        #     db.session.commit()
        #     # token_de_acceso = create_access_token(identity=nuevo_usuario.id)
        #     return {"mensaje": "usuario creado exitosamente", "id": nuevo_entrenador.id}
        # else:
        return "El usuario ya existe", 404


class VistaLogIn(Resource):

    def post(self):
        # contrasena_encriptada = hashlib.md5(
        #     request.json["contrasena"].encode('utf-8')).hexdigest()
        # persona = Persona.query.filter(Persona.usuario == request.json["usuario"],
        #                                Persona.contrasena == contrasena_encriptada).first()
        # 
        # db.session.commit()
        # if persona is None:          
        #     return "El usuario no existe", 404
        # else:
        #     
        #     objeto_persona = persona_schema.dump(persona)
        #     print("usuario si existe--------", objeto_persona)
        #     del objeto_persona['contrasena']
        #     rol_persona = None
        #     if objeto_persona['rol'] is not None and objeto_persona['rol']['llave'] is not None:
        #         del objeto_persona['rol']['llave']
        #         rol_persona = objeto_persona['rol']['valor']
        #     token_de_acceso = create_access_token(identity=objeto_persona)
        #    return {"mensaje": "Inicio de sesión exitoso", "token": token_de_acceso, "id": persona.id, "rol": rol_persona}
        return "Login", 200


def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def to_zip():
    print("Im a zip")

def to_tar_bz2():
    print("Im a tar bz2")

def to_tar_gz():
    print("im a tar gz")

class VistaCreateTasks(Resource):

    def post(self):
        UPLOAD_FOLDER = './uploads'
        destination_format = request.form.get("to_format")
        print(f'to format -> {destination_format}')
        formats = {
            'zip': to_zip,
            'tar_gz': to_tar_gz,
            'tar_bz2': to_tar_bz2
        }

        if destination_format in formats.keys():
            print(f"calling {destination_format}")
            func = formats[destination_format]
            print(f"function: {func}")
            func()
        else:
            print("Invalid format")

        # check if the post request has the file part
        if 'file' not in request.files:
            # flash('No file part')
            return 'No file part'#redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            # flash('No selected file')
            return 'No selected file'# redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            #return redirect(url_for('download_file', name=filename))
            # return url_for('download_file', name=filename)

        filename = file.filename# request.json["fileName"]
        extension = filename.split('.')
        response_string = f'Filename: {filename}, extension: {extension[-1]}'
        # with zipfile.ZipFile("./processed/data.zip", "a") as zip:
        #     zip.write("vinyl.png ", arcname="./app.py")
        with zipfile.ZipFile("./processed/data.zip", "a") as zip:
            # Add the uploaded file to the archive
            zip.write(os.path.join(UPLOAD_FOLDER, filename), arcname=filename)

        return response_string, 200

class VistaFile(Resource):
    def get(self, name):
        UPLOAD_FOLDER = './uploads'
        return send_from_directory(UPLOAD_FOLDER, name)