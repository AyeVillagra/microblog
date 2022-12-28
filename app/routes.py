#funcion que invoca el motor de plantilas Jinja2; sustituye en el renderizado los bloques con los
#valores correspondientes dados por los argumentos proporcionados en la llamada de la función (línea 19)

from flask import render_template, flash, redirect, url_for, request
from app import app
from app import db
from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, login_required, logout_user
from app.models import User
from werkzeug.urls import url_parse

@app.route('/')
@app.route('/index')
@login_required #protege la vista (la función está protegida), dejando solo acceso a los usuarios logueados
def index():
    user = {'username': 'Miguel'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home', posts=posts) #si no se pasa un valor para title, la plantilla da uno predeterminado

@app.route('/login', methods=['GET', 'POST'])
# el methods indica qué métodos de solicitud acepta
def login():
    if current_user.is_authenticated: #current_user, variable utilizada para obtener el objeto usuario que representa al cliente que hace la petición
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data) #función que registra al usuario como conectado
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '': #url_parse determina si una url es relativa o absoluta
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title ='Sign In', form=form)

# cuando el método es get(pide la pág con el formulario), devuelve false y lleva hasta el formulario
# cuando el método es post y se clickea ENVIAR, la función recopila los datos y los valida, devolviendo true
#         flash('Login requested for user {}, remember_me={}'.format(
#             form.username.data, form.remember_me.data))
#
# si la función anterior devuelve true, se llama a dos nuevas funciones. La FLASH envía un mensaje al usuario
#         return redirect(url_for('index'))
#
# la función redirect (tmb se utiliza cuando form.validate_on_submit da true), lleva automáticamente a otra página dada como argumento
#     return render_template('login.html',  title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

