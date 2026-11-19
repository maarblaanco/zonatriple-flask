from flask import Blueprint, request, redirect, render_template, session, flash
from models import User
from database import db

auth_bp = Blueprint('auth', __name__, template_folder='../templates/auth')


# REGISTER VIEW
@auth_bp.route('/register', methods=['GET'])
def register_view():
    return render_template('register.html')


# REGISTER
@auth_bp.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']

    # Email único
    if User.query.filter_by(email=email).first():
        flash('El email ya está registrado.', 'error')
        return redirect('/auth/register')
    
    # Username único
    if User.query.filter_by(username=username).first():
        flash('El nombre de usuario ya está registrado.', 'error')
        return redirect('/auth/register')

    new_user = User(username=username, email=email)
    new_user.set_password(password)

    db.session.add(new_user)
    db.session.commit()

    flash('Registro exitoso, ahora puedes iniciar sesión.', 'success')
    return redirect('/auth/login')


# LOGIN VIEW
@auth_bp.route('/login', methods=['GET'])
def login_view():
    return render_template('login.html')


# LOGIN
@auth_bp.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    user = User.query.filter_by(email=email).first()

    if user and user.check_password(password):
        session['user'] = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role
        }
        flash('Inicio de sesión exitoso.', 'success')
        return redirect('/')
    else:
        flash('Correo o contraseña incorrectos.', 'error')
        return redirect('/auth/login')


# LOGOUT 
@auth_bp.route('/logout')
def logout():
    session.pop('user', None)
    flash('Sesión cerrada correctamente.', 'success')
    return redirect('/')