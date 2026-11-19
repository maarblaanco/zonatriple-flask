from flask import Blueprint, render_template, request, redirect, abort
from functools import wraps

from models import User
from database import db

from access_control import check_session, check_role

usuarios_bp = Blueprint('usuarios', __name__)


@usuarios_bp.before_request
@check_session
@check_role
def before_request_usuarios_bp():
    pass


@usuarios_bp.after_request
def agregar_total_usuarios(response):
    response.headers["X-Total-Usuarios"] = User.query.count()
    return response

# AUTOLOAD
def load_usuario(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        usuarioId = request.view_args.get('usuarioId')
        if usuarioId is not None:
            usuario_requested = User.query.filter_by(id=usuarioId).first()
            if usuario_requested is None:
                abort(404)
            kwargs['usuario'] = usuario_requested
        return f(*args, **kwargs)
    return decorated_function


# LIST
@usuarios_bp.route('/', methods=['GET'])
def list():
    usuarios = User.query.all()
    return render_template('usuarios/list.html', usuarios=usuarios)


# NEW
@usuarios_bp.route('/new', methods=['GET'])
def new():
    return render_template('usuarios/new.html')


# CREATE
@usuarios_bp.route('/', methods=['POST'])
def create():
    user = User(
        username=request.form.get("username"),
        email=request.form.get("email"),
        role=request.form.get("role", "user")
    )

    user.set_password(request.form.get("password"))

    db.session.add(user)
    db.session.commit()

    return redirect('/usuarios')


# SHOW
@usuarios_bp.route('/<usuarioId>', methods=['GET'])
@load_usuario
def show(usuarioId, usuario):
    return render_template('usuarios/show.html', usuario=usuario)


# EDIT
@usuarios_bp.route('/<usuarioId>/edit', methods=['GET'])
@load_usuario
def edit(usuarioId, usuario):
    return render_template('usuarios/edit.html', usuario=usuario)


# UPDATE
@usuarios_bp.route('/<usuarioId>', methods=['PUT'])
@load_usuario
def update(usuarioId, usuario):
    usuario.username = request.form.get('username')
    usuario.email = request.form.get('email')
    usuario.role = request.form.get('role', usuario.role)

    password = request.form.get('password', '').strip()
    if password:
        usuario.set_password(password)

    db.session.commit()
    return redirect('/usuarios')


# DELETE
@usuarios_bp.route('/<usuarioId>', methods=['DELETE'])
@load_usuario
def delete(usuarioId, usuario):
    db.session.delete(usuario)
    db.session.commit()
    return redirect('/usuarios')