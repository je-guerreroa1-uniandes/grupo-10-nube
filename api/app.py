from flask import Flask

# from .modelos import db, PuntoVenta
from vistas import VistaHealthCheck, VistaSignIn, VistaLogIn, VistaCreateTasks, VistaFile
from flask_restful import Api

app = Flask(__name__)
app_context = app.app_context()
app_context.push()

# db.init_app(app)
# db.create_all()   
   
api = Api(app)

api.add_resource(VistaHealthCheck, '/api')

# User management
api.add_resource(VistaSignIn, '/api/auth/signup')
api.add_resource(VistaLogIn, '/api/auth/login')

# Tasks management
api.add_resource(VistaCreateTasks, '/api/tasks')

# File management
api.add_resource(VistaFile, '/api/files/<name>')