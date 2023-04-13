from flask import Flask
# from .modelos import db, PuntoVenta
from vistas import VistaSignIn, VistaLogIn
from flask_restful import Api

app = Flask(__name__)
app_context = app.app_context()
app_context.push()

# db.init_app(app)
# db.create_all()   
   
api = Api(app)
api.add_resource(VistaSignIn, '/register')
api.add_resource(VistaLogIn, '/login')