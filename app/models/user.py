import uuid
from database import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    username = db.Column(db.String(255), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)

    password_hash = db.Column(db.String(255), nullable=False)

    role = db.Column(db.Enum("admin", "user", name="role_enum"), nullable=False, default="user")

    equipos = db.relationship("Equipo", backref="user", lazy=True)

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)