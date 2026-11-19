# ZonaTriple · Flask + SQLAlchemy + API REST

Aplicación web para gestionar equipos de baloncesto (ACB, Liga Femenina Endesa y LEB), con usuarios, roles, subida de imágenes y una **API REST documentada con OpenAPI**. Proyecto de la asignatura Tecnologías Web (Grado en Ingeniería de Sistemas de Datos, ETSIT-UPM), desarrollado de forma incremental a lo largo de cinco prácticas.

## Qué hace

**Aplicación web**
- Alta, consulta, edición y borrado de equipos, con filtros por nombre y por liga.
- Registro, inicio y cierre de sesión. Las contraseñas se guardan con hash (Werkzeug).
- **Control de acceso por rol:** un administrador gestiona todos los equipos y los usuarios; un usuario normal solo ve y modifica sus propios equipos.
- Subida de un escudo por equipo: validación de extensión (png, jpg, jpeg) y de tamaño (máx. 5 MB), nombre único con UUID y miniatura de 150×150 generada con Pillow. Al borrar o sustituir un equipo se eliminan los ficheros antiguos.
- Páginas de error 404 y 500 personalizadas.

**API REST (`/api/v1`)**

| Método | Ruta | Descripción |
|---|---|---|
| GET | `/api/v1/equipos` | Lista todos los equipos |
| GET | `/api/v1/equipos/{id}` | Devuelve un equipo e incluye el **tiempo actual de su ciudad**, consultado de forma asíncrona a Open-Meteo y cacheado 10 minutos |
| POST | `/api/v1/equipos` | Crea un equipo (validación con Pydantic) |
| PUT | `/api/v1/equipos/{id}` | Actualiza campos de un equipo |
| DELETE | `/api/v1/equipos/{id}` | Elimina un equipo |

Las entradas y salidas se validan con **DTOs de Pydantic**, los errores de validación devuelven un 400 con el detalle, y cada petición queda registrada con `logging` (consola y fichero `api.log`). La documentación interactiva (Swagger UI) se genera con Flasgger a partir de `app/openapi.yaml`.

## Cómo se construyó

| Práctica | Qué se añadió |
|---|---|
| 1 | Maquetación estática en HTML y CSS |
| 2 | Flask, plantillas Jinja, blueprints y `method_override` para PUT y DELETE desde formularios |
| 3 | Subida de ficheros, validaciones y miniaturas |
| 4 | Base de datos con SQLAlchemy (MySQL), migraciones con Alembic, login y control de acceso por rol |
| 5 | API REST con OpenAPI, DTOs, logging y consumo asíncrono de una API externa |

## Estructura

```
app/
├── app.py                  Configuración, registro de blueprints y comando seed
├── access_control.py       Decoradores de sesión y permisos por rol
├── database.py             Instancia de SQLAlchemy
├── handle_files.py         Subida de imágenes y generación de miniaturas
├── logger.py               Configuración de logging
├── blueprints/             Rutas: equipos, usuarios, auth y api_v1
├── models/                 Modelos, migraciones (Alembic) y seeders
├── dtos/                   DTOs de Pydantic para la API
├── services/               Cliente asíncrono de Open-Meteo
├── templates/ y public/    Vistas, estilos, fuentes e imágenes
└── openapi.yaml            Especificación de la API
client/client.py            Cliente de ejemplo de la API con httpx
requirements.txt
```

## Tecnologías

Python · Flask · SQLAlchemy / Flask-SQLAlchemy · MySQL · Alembic (Flask-Migrate) · Pydantic · Flasgger / OpenAPI 3 · httpx · aiocache · Pillow · Jinja2 · HTML y CSS

## Cómo ejecutarlo

Necesitas Python 3 y un servidor MySQL en local. Todos los comandos se lanzan desde la raíz del repositorio.

```bash
# 1. Entorno virtual y dependencias
python -m venv venv
source venv/bin/activate          # En Windows: .\venv\Scripts\activate
pip install -r requirements.txt

# 2. Configuración (opcional, estos son los valores por defecto)
export DATABASE_URL="mysql+mysqlconnector://root:root@localhost/practica4_db"
export SECRET_KEY="una-clave-larga-y-aleatoria"

# 3. Crear tablas y datos de ejemplo (la base de datos se crea si no existe)
flask --app app/app.py db upgrade
flask --app app/app.py seed

# 4. Arrancar
flask --app app/app.py run
```

Abre `http://localhost:5000`. La documentación de la API está en `http://localhost:5000/apidocs/`.

**Usuarios de demostración** (ficticios, creados por el seeder, solo para desarrollo local; se entra con el correo):

| Rol | Correo | Contraseña |
|---|---|---|
| admin | `admin@zonatriple.es` | `admin123` |
| user | `mar.blanco@zonatriple.es` | `mar123` |

El cliente de ejemplo (`python client/client.py`) necesita la app en marcha y un `user_id` real de tu base de datos en la función `create_equipo`.

## Posibles mejoras

- Proteger la API con autenticación (por ejemplo, tokens JWT): ahora mismo cualquiera puede llamar a sus endpoints.
- Añadir protección CSRF a los formularios.
- Escribir tests automáticos con `pytest` y una base de datos de pruebas.
- Dockerizar la app con un `docker-compose` que incluya MySQL.
- Sustituir `Query.get` (API antigua de SQLAlchemy) por `db.session.get`.
- Añadir paginación en los listados.

## Imágenes

Los escudos de los clubes y las fotografías se usan con fines exclusivamente docentes. Sus derechos pertenecen a sus respectivos propietarios.
