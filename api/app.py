from flask import Flask

from .vistas import VistaSignIn, VistaLogIn
from flask_restful import Api

from flask import request
from .modelos import db

# from .modelos import Usuario, UsuarioSchema

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///conversion_tools.db'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
app_context = app.app_context()  # Hacer push del contexto de la app
app_context.push()

# app = Flask(__name__)
# app_context = app.app_context()
# app_context.push()

db.init_app(app)  # Inicializacion base de datos
db.create_all()

api = Api(app)
api.add_resource(VistaSignIn, '/signin')
api.add_resource(VistaLogIn, '/login')


# PRUEBA
# with app.app_context():
#   u1 = Usuario(nombre='Pepito', contrasena='123', email='pepito@correo.com')
#   db.session.add(u1)
#   db.session.commit()
#   print(Usuario.query.all())
