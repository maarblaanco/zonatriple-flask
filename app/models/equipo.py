from database import db

class Equipo(db.Model):
    __tablename__ = "equipo"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    nombre = db.Column(db.String(255), nullable=False)
    ciudad = db.Column(db.String(255), nullable=True)
    fundacion = db.Column(db.Integer, nullable=True)
    liga = db.Column(db.String(255), nullable=True)
    pabellon = db.Column(db.String(255), nullable=True)
    aforo = db.Column(db.Integer, nullable=True)
    cantera = db.Column(db.Boolean, default=False)

    filename = db.Column(db.String(120), nullable=True, unique=True)

    user_id = db.Column(db.String(36), db.ForeignKey("user.id"), nullable=False)