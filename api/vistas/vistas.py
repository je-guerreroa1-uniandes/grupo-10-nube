from flask import request
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from flask_restful import Resource
# from sqlalchemy.exc import IntegrityError
# from sqlalchemy import and_
# from datetime import datetime
# import hashlib

from ..modelos import db, Usuario, UsuarioSchema

usuario_schema = UsuarioSchema()  # Instanciar esquema creado


# class Usuario(db.Model):
#   id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(50))
#     password = db.Column(db.String(50))
#     email = db.Column(db.String(128))


class VistaSignIn(Resource):
  def post(self):
    nuevo_usuario = Usuario(username=request.json['username'],
                            password=request.json['password'],
                            email=request.json['email'])

    # token_de_acceso = create_access_token(identity=request.json['nombre'])

    db.session.add(nuevo_usuario)
    db.session.commit()
    return 'Usuario creado exitosamente', 201

    # return {'mensaje': 'usuario creado exitosamente', 'token_de_acceso': token_de_acceso}

  def put(self, id_usuario):
    usuario = Usuario.query.get_or_404(id_usuario)
    usuario.username = request.json.get('username', usuario.username)
    usuario.password = request.json.get('password', usuario.password)
    usuario.email = request.json.get('email', usuario.email)
    db.session.commit()
    return usuario_schema.dump(usuario)

  def delete(self, id_usuario):
    usuario = Usuario.query.get_or_404(id_usuario)
    db.session.delete(usuario)
    db.session.commit()
    return 'Operacion exitosa', 204



# class VistaSignIn(Resource):

#     def post(self):
    #     entrenador = Entrenador.query.filter(
    #         Entrenador.usuario == request.json["usuario"]).first()
    #     if entrenador is None:
    #         contrasena_encriptada = hashlib.md5(
    #             request.json["contrasena"].encode('utf-8')).hexdigest()
    #         nuevo_entrenador = Entrenador(
    #             usuario=request.json["usuario"], contrasena=contrasena_encriptada, rol=Rol.ENTRENADOR)
    #         db.session.add(nuevo_entrenador)
    #         db.session.commit()
    #         # token_de_acceso = create_access_token(identity=nuevo_usuario.id)
    #         return {"mensaje": "usuario creado exitosamente", "id": nuevo_entrenador.id}
    #     else:
            # return "El usuario ya existe", 404

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