import os
import uuid
from functools import wraps
from flask import request, redirect, flash, current_app

from PIL import Image


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


def _save_thumbnail(image_path, thumb_path):
    with Image.open(image_path) as img:
        img.thumbnail((150, 150))
        img.save(thumb_path)


def save_file(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):

        file = request.files['file'] if 'file' in request.files else None
        kwargs['filename'] = None

        if file and file.filename != "":
            # Validar extensión
            if not allowed_file(file.filename):
                flash("Extensión no permitida", "error")
                return redirect(request.url)

            # Validar tamaño (5MB)
            file.seek(0, os.SEEK_END)
            size = file.tell()
            file.seek(0)

            if size > current_app.config['MAX_FILE_SIZE']:
                flash("El fichero supera los 5MB", "error")
                return redirect(request.url)

            # Generar UUID
            extension = file.filename.rsplit('.', 1)[1].lower()
            filename = f"{uuid.uuid4()}.{extension}"
            kwargs['filename'] = filename

            # Guardar imagen
            image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(image_path)

            # Crear thumbnail
            thumb_path = os.path.join(current_app.config['THUMBNAIL_FOLDER'], filename)
            _save_thumbnail(image_path, thumb_path)

        return f(*args, **kwargs)

    return decorated_function


def delete_file(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        equipo = kwargs['equipo']  

        filename = equipo.filename
        if filename:
            image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            thumb_path = os.path.join(current_app.config['THUMBNAIL_FOLDER'], filename)

            # Estando en update y no se ha subido archivo nuevo, no borra
            file = request.files.get('file')
            if file is not None and (not file.filename):
                return f(*args, **kwargs)

            if os.path.exists(image_path):
                os.remove(image_path)

            if os.path.exists(thumb_path):
                os.remove(thumb_path)

        return f(*args, **kwargs)
    return decorated_function