#Este archivo es usado para verificar los datos en la base de datos.
#Es un archivo de prueba y se podria prescindir de el

from db import session
from models import User, Game, Participant, Result

def print_data():
    games = session.query(Game).all()
    for game in games:
        print(f"Game: {game.name}")
        participants = session.query(Participant).filter_by(game_id=game.id).all()
        for participant in participants:
            user = session.get(User, participant.user_id)
            print(f"  Participant: {user.username} ({participant.level})")
            results = session.query(Result).filter_by(participant_id=participant.id).all()
            for result in results:
                print(f"    Score: {result.score}, Time: {result.time}")

if __name__ == "__main__":
    print_data()

