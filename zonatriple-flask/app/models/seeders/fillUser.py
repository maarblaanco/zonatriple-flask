from database import db
from models import User

def fillUser():
    admin = User(username="admin", email="admin@zonatriple.es", role="admin")
    admin.set_password("admin123")

    user1 = User(username="mar.blanco", email="mar.blanco@zonatriple.es", role="user")
    user1.set_password("mar123")

    user2 = User(username="carlos.lopez", email="carlos.lopez@zonatriple.es", role="user")
    user2.set_password("carlos123")

    db.session.add(admin)
    db.session.add(user1)
    db.session.add(user2)
    db.session.commit()

    print("User data inserted successfully.")