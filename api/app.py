from flask import Flask

# from .modelos import db, PuntoVenta
from vistas import VistaHealthCheck, VistaSignIn, VistaUpdateSignIn, VistaLogIn, VistaCreateTasks, VistaFile, VistaGetTask
from flask_restful import Api

from flask import request
from modelos import db
from flask_jwt_extended import JWTManager

import config

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config.POSTGRES_URI
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

app.config['JWT_SECRET_KEY'] = config.G10_JWT_SECRET
app.config['PROPAGATE_EXCEPTIONS'] = True
# Para sacar un token de pruebas
# app.config["JWT_ACCESS_TOKEN_EXPIRES"] = False

app_context = app.app_context()  # Hacer push del contexto de la app
app_context.push()

db.init_app(app)  # Inicializacion base de datos
db.create_all()

api = Api(app)

api.add_resource(VistaHealthCheck, '/api')

# User management
api.add_resource(VistaSignIn, '/api/auth/signup')
api.add_resource(VistaUpdateSignIn, '/api/auth/signup/<int:id_usuario>')
api.add_resource(VistaLogIn, '/api/auth/login')


# Tasks management
api.add_resource(VistaCreateTasks, '/api/tasks')
api.add_resource(VistaGetTask, '/api/tasks/<task_id>')

# File management
api.add_resource(VistaFile, '/api/files/<filename>')

jwt = JWTManager(app)
