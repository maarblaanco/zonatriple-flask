from flask import Blueprint, render_template, request, redirect, abort, flash, session
import re
from functools import wraps

from handle_files import save_file, delete_file
from models import Equipo
from database import db
from access_control import check_session, check_role

equipos_bp = Blueprint('equipos', __name__)

ligas = ["ACB", "Liga Femenina Endesa", "LEB"]


# VALIDACIONES
def nombre_valido(nombre: str) -> bool:
    if not nombre:
        return False
    return re.search(r"[\/=\(\)]", nombre) is None


# CONTROL DE ACCESO 
@equipos_bp.before_request
@check_session
@check_role
def before_request_equipos_bp():
    pass


@equipos_bp.after_request
def agregar_total_equipos(response):
    response.headers["X-Total-Equipos"] = Equipo.query.count()
    return response


# AUTOLOAD
def load_equipo(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        equipoId = request.view_args.get('equipoId')

        if equipoId is not None:
            if not str(equipoId).isdigit():
                abort(404)

            role = session['user']['role']
            user_id = session['user']['id']

            query = Equipo.query.filter_by(id=int(equipoId))
            if role != "admin":
                query = query.filter_by(user_id=user_id)

            equipo_requested = query.first()
            if equipo_requested is None:
                abort(404)

            kwargs['equipo'] = equipo_requested

        return f(*args, **kwargs)
    return decorated_function

# LIST
@equipos_bp.route('/', methods=['GET'])
def list():
    nombre_raw = request.args.get('nombre', '').strip()
    liga = request.args.get('liga', '').strip()

    if nombre_raw and not nombre_valido(nombre_raw):
        flash("Nombre no válido: evita caracteres especiales como / = ( )", "error")
        return redirect('/equipos')

    query = Equipo.query

    role = session['user']['role']
    user_id = session['user']['id']

    if role != "admin":
        query = query.filter(Equipo.user_id == user_id)

    if nombre_raw:
        query = query.filter(Equipo.nombre.like(f"%{nombre_raw}%"))

    if liga:
        query = query.filter(Equipo.liga == liga)

    equipos_filtrados = query.all()

    return render_template(
        'equipos/list.html',
        equipos=equipos_filtrados,
        ligas=ligas,
        filtros={"nombre": nombre_raw, "liga": liga}
    )


# NEW
@equipos_bp.route('/new', methods=['GET'])
def new():
    return render_template('equipos/new.html', ligas=ligas)


# CREATE
@equipos_bp.route('/', methods=['POST'])
@save_file
def create(filename):

    nombre = request.form.get("nombre", "").strip()
    aforo_str = request.form.get("aforo", "").strip()

    # Validar liga
    liga = request.form.get("liga")
    if liga not in ligas:
        abort(400)

    # Validar nombre
    if not nombre_valido(nombre):
        flash("Nombre no válido: no uses / = ( )", "error")
        return redirect("/equipos/new")

    # Validar aforo
    try:
        aforo = int(aforo_str)
    except ValueError:
        aforo = -1

    if aforo < 0 or aforo > 30000:
        flash("Aforo no válido: debe estar entre 0 y 30000", "error")
        return redirect("/equipos/new")

    equipo = Equipo(
        nombre=nombre,
        ciudad=request.form.get("ciudad"),
        fundacion=int(request.form.get("fundacion")),
        liga=liga,
        pabellon=request.form.get("pabellon"),
        aforo=aforo,
        cantera=True if request.form.get("cantera") == "on" else False,
        filename=filename,
        user_id=session['user']['id']
    )

    db.session.add(equipo)
    db.session.commit()

    flash("Equipo creado correctamente", "success")
    return redirect('/equipos')


# SHOW
@equipos_bp.route('/<equipoId>', methods=['GET'])
@load_equipo
def show(equipoId, equipo):
    return render_template('equipos/show.html', equipo=equipo)


# EDIT
@equipos_bp.route('/<equipoId>/edit', methods=['GET'])
@load_equipo
def edit(equipoId, equipo):
    return render_template('equipos/edit.html', equipo=equipo, ligas=ligas)


# UPDATE
@equipos_bp.route('/<equipoId>/update', methods=['PUT'])
@load_equipo
@delete_file
@save_file
def update(equipoId, equipo, filename):

    nombre = request.form.get("nombre", "").strip()
    aforo_str = request.form.get("aforo", "").strip()

    # Validar liga
    liga = request.form.get("liga")
    if liga not in ligas:
        abort(400)

    # Validar nombre
    if not nombre_valido(nombre):
        flash("Nombre no válido: no uses / = ( )", "error")
        return redirect(f"/equipos/{equipoId}/edit")

    # Validar aforo
    try:
        aforo = int(aforo_str)
    except ValueError:
        aforo = -1

    if aforo < 0 or aforo > 30000:
        flash("Aforo no válido: debe estar entre 0 y 30000", "error")
        return redirect(f"/equipos/{equipoId}/edit")

    equipo.nombre = nombre
    equipo.ciudad = request.form.get('ciudad')
    equipo.fundacion = int(request.form.get('fundacion'))
    equipo.liga = liga
    equipo.pabellon = request.form.get('pabellon')
    equipo.aforo = aforo
    equipo.cantera = True if request.form.get('cantera') == 'on' else False

    if filename:
        equipo.filename = filename

    db.session.commit()

    flash("Equipo actualizado correctamente", "success")
    return redirect('/equipos')

# DELETE
@equipos_bp.route('/<equipoId>/delete', methods=['DELETE'])
@load_equipo
@delete_file
def delete(equipoId, equipo):
    db.session.delete(equipo)
    db.session.commit()

    flash("Equipo eliminado correctamente", "success")
    return redirect('/equipos')