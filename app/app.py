import os
import click
import logging
from logger import logger
from flask import Flask, render_template, send_from_directory
from flask.cli import with_appcontext
from flasgger import Swagger

from method_override import MethodOverrideMiddleware
from blueprints.equipos import equipos_bp
from blueprints.usuarios import usuarios_bp
from blueprints.auth import auth_bp
from blueprints.api_v1 import api_v1

from sqlalchemy_utils import create_database, database_exists
from flask_migrate import Migrate
from database import db

from models import Equipo, User

app = Flask(__name__, static_folder='public', static_url_path="", template_folder='templates')
app.secret_key = os.getenv("SECRET_KEY", "dev-only-change-me")

app.config['SWAGGER'] = {
    'title': 'API ZonaTriple',
    'uiversion': 3,
    'openapi': '3.0.3'
}

swagger = Swagger(app, template_file='openapi.yaml')

app.logger.handlers.clear()
for handler in logger.handlers:
    app.logger.addHandler(handler)
app.logger.setLevel(logging.INFO)

werkzeug_logger = logging.getLogger("werkzeug")
werkzeug_logger.handlers.clear()
for handler in logger.handlers:
    werkzeug_logger.addHandler(handler)
werkzeug_logger.setLevel(logging.INFO)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL", "mysql+mysqlconnector://root:root@localhost/practica4_db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

if not database_exists(app.config['SQLALCHEMY_DATABASE_URI']):
    create_database(app.config['SQLALCHEMY_DATABASE_URI'])

migrate = Migrate(app, db, directory="app/models/migrations")

# PRIVATE - File configuration
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'assets/images')
app.config['THUMBNAIL_FOLDER'] = os.path.join(app.root_path, 'assets/thumbnails')
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}
app.config['MAX_FILE_SIZE'] = 5 * 1024 * 1024  # 5MB

# Si no existen carpetas se crean
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['THUMBNAIL_FOLDER'], exist_ok=True)

app.wsgi_app = MethodOverrideMiddleware(app.wsgi_app)

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/about", methods=["GET"])
def about():
    return render_template("about.html")

@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/thumbnail/<filename>')
def thumbnail(filename):
    return send_from_directory(app.config['THUMBNAIL_FOLDER'], filename)

app.register_blueprint(equipos_bp, url_prefix="/equipos")
app.register_blueprint(usuarios_bp, url_prefix="/usuarios")
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(api_v1)

@app.errorhandler(404)
def page_not_found(e):
    return render_template("error404.html"), 404

@app.errorhandler(500)
def internal_error(e):
    return render_template("error500.html"), 500

# SEED COMMAND 
@click.command(name='seed')
@with_appcontext
def seed():
    from models.seeders import fillUser, fillEquipo
    fillUser()
    fillEquipo()

app.cli.add_command(seed)

if __name__ == "__main__":
    app.run(debug=True)