from flask import Flask

from .vistas import VistaSignIn, VistaLogIn
from flask_restful import Api

from flask import request
from .modelos import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///conversion_tools.db'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
app_context = app.app_context()  # Hacer push del contexto de la app
app_context.push()

db.init_app(app)  # Inicializacion base de datos
db.create_all()

api = Api(app)
api.add_resource(VistaSignIn, '/signin')
api.add_resource(VistaLogIn, '/login')
