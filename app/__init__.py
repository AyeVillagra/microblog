from flask import Flask #importo del paquete flask, la clase Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app) #objeto que representa la BD
migrate = Migrate(app, db) #objeto que representa el motor de migración
login = LoginManager(app)
login.login_view = 'login' #para implementar el inicio de sesión requerido para ver determinada página

from app import routes, models
#models = módulo que define la estructura de la base de datos