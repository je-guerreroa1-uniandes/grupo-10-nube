from flask import Flask

# from .modelos import db, PuntoVenta
from vistas import VistaHealthCheck, VistaSignIn, VistaLogIn, VistaCreateTasks, VistaFile
from flask_restful import Api

from flask import request
from .modelos import db
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///conversion_tools.db'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

app.config['JWT_SECRET_KEY'] = 'frase-secreta-grupo-10-nube'
app.config['PROPAGATE_EXCEPTIONS']= True


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

# File management
api.add_resource(VistaFile, '/api/files/<name>')

jwt = JWTManager(app)
