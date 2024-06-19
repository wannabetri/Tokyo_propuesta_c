#Este archivo inicializa los datos en la base de datos. Se usa para agregar juegos y usuarios iniciales.
#Es un archivo de prueba y se podria prescindir de el

from db import session
from models import User, Game, Participant, Result
from datetime import timedelta

#Crear juegos basicos
lol = Game(name="League of Legends", description="League of Legends es uno de los deportes electrónicos más grandes del mundo.")
dota2 = Game(name="Dota 2", description="Dota 2 es un juego multijugador de arena de batalla en línea, desarrollado por Valve Corporation.")
csgo = Game(name="Counter-Strike: Global Offensive", description="Counter-Strike: Global Offensive es un juego de disparos en primera persona.")

#Añadir juegos a la base de datos
session.add_all([lol, dota2, csgo])
session.commit()

#Creamos usuarios y participantes
users = [
    User(username="admin", email="admin@example.com", is_admin=True),
    User(username="player1", email="player1@example.com"),
    User(username="player2", email="player2@example.com"),
    User(username="player3", email="player3@example.com"),
    User(username="playerA", email="playerA@example.com"),
    User(username="playerB", email="playerB@example.com"),
    User(username="playerC", email="playerC@example.com"),
]

#Establecemos contraseñas
passwords = {
    "admin": "adminpassword",
    "player1": "password1",
    "player2": "password2",
    "player3": "password3",
    "playerA": "passwordA",
    "playerB": "passwordB",
    "playerC": "passwordC",
}

for user in users:
    user.set_password(passwords[user.username])

#Añadimos usuarios a la base de datos
session.add_all(users)
session.commit()

#Creamos los participantes
participants = [
    Participant(user_id=users[1].id, game_id=lol.id, level="Diamond"),
    Participant(user_id=users[2].id, game_id=lol.id, level="Platinum"),
    Participant(user_id=users[3].id, game_id=lol.id, level="Gold"),
    Participant(user_id=users[4].id, game_id=dota2.id, level="Diamond"),
    Participant(user_id=users[5].id, game_id=dota2.id, level="Platinum"),
    Participant(user_id=users[6].id, game_id=dota2.id, level="Gold"),
    Participant(user_id=users[1].id, game_id=csgo.id, level="Diamond"),
    Participant(user_id=users[2].id, game_id=csgo.id, level="Platinum"),
    Participant(user_id=users[3].id, game_id=csgo.id, level="Gold"),
]

#Añadimos los participantes a la base de datos
session.add_all(participants)
session.commit()

#Creamos los resultados
results = [
    Result(participant_id=participants[0].id, score=1000, time=timedelta(minutes=30)),
    Result(participant_id=participants[1].id, score=850, time=timedelta(minutes=35)),
    Result(participant_id=participants[2].id, score=900, time=timedelta(minutes=32)),
    Result(participant_id=participants[3].id, score=1200, time=timedelta(minutes=25)),
    Result(participant_id=participants[4].id, score=950, time=timedelta(minutes=33)),
    Result(participant_id=participants[5].id, score=1100, time=timedelta(minutes=28)),
    Result(participant_id=participants[6].id, score=1300, time=timedelta(minutes=20)),
    Result(participant_id=participants[7].id, score=1050, time=timedelta(minutes=30)),
    Result(participant_id=participants[8].id, score=1250, time=timedelta(minutes=25)),
]

#Añadimos los resultados a la base de datos
session.add_all(results)
session.commit()