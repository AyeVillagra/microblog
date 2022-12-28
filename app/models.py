from app import db
from app import login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin #clase que incluye implementaciones genéricas para los modelos de usuario

@login.user_loader
def load_user(id):
    return User.query.get(int(id)) #este id es un string - ver compatbilidad con la DB

#db.Model es una clase base de flask-sqlalchemy
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128)) #por seguridad se guarda el hash
    posts = db.relationship('Post', backref='author', lazy='dynamic')

#método que indica cómo imprimir objetos de esta clase
    def __repr__(self):
        return '<User {}>'.format(self.username)

#métodos de hashing de contraseña
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow) #datetime.utcnow incluye la función no el resultado de llamarla
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)