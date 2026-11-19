from database import db
from models import Equipo, User

def fillEquipo():
    user1 = User.query.filter_by(username="mar.blanco").first()
    user2 = User.query.filter_by(username="carlos.lopez").first()

    equipo1 = Equipo(
        nombre="Real Madrid",
        ciudad="Madrid",
        fundacion=1931,
        liga="ACB",
        pabellon="Movistar Arena",
        aforo=17000,
        cantera=True,
        filename=None,
        user_id=user1.id
    )

    equipo2 = Equipo(
        nombre="FC Barcelona",
        ciudad="Barcelona",
        fundacion=1926,
        liga="ACB",
        pabellon="Palau Blaugrana",
        aforo=7500,
        cantera=True,
        filename=None,
        user_id=user1.id
    )

    equipo3 = Equipo(
        nombre="Leyma Coruña",
        ciudad="A Coruña",
        fundacion=1996,
        liga="LEB",
        pabellon="Coliseum",
        aforo=9000,
        cantera=False,
        filename=None,
        user_id=user2.id
    )

    db.session.add(equipo1)
    db.session.add(equipo2)
    db.session.add(equipo3)
    db.session.commit()

    print("Equipo data inserted successfully.")