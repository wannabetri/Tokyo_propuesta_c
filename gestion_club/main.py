#Este archivo es el núcleo de la aplicación Flask.
# Define las rutas y las vistas, gestiona la autenticación de usuarios y maneja la lógica principal de la aplicación.

import base64
import io
import matplotlib.pyplot as plt  # Importa Matplotlib para crear gráficos
from flask import Flask, render_template, redirect, url_for, request, flash  # Importa elementos necesarios de Flask
from flask_login import LoginManager, login_user, login_required, current_user, logout_user  # Importa elementos de Flask-Login
from db import session  # Importa la sesión de la base de datos
from models import User, Game, Participant, Result  # Importa los modelos de la base de datos

app = Flask(__name__)  # Crea una instancia de la aplicación Flask
app.secret_key = 'your_secret_key'  # Configura la clave secreta para la aplicación

login_manager = LoginManager()  # Crea un objeto LoginManager para gestionar la autenticación de usuarios
login_manager.init_app(app)  # Inicializa el objeto LoginManager con la aplicación Flask
login_manager.login_view = "login"  # Configura la vista de inicio de sesión

# Función para cargar un usuario dado su ID
@login_manager.user_loader
def load_user(user_id):
    return session.get(User, user_id)

# Vista para la página de inicio
@app.route("/")
@login_required  # Requiere que el usuario esté autenticado para acceder a esta ruta
def home():
    user_games = session.query(Game).join(Participant).filter(Participant.user_id == current_user.id).all()
    user_scores = {}
    for game in user_games:
        result = session.query(Result).join(Participant).filter(Participant.game_id == game.id, Participant.user_id == current_user.id).first()
        user_scores[game.name] = result.score if result else "No score yet"

    all_games = session.query(Game).all()
    available_games = [game for game in all_games if game not in user_games]

    return render_template("home.html", user_scores=user_scores, available_games=available_games)

# Vista para la página de perfil del usuario
@app.route("/profile")
@login_required
def profile():
    user_games = session.query(Game).join(Participant).filter(Participant.user_id == current_user.id).all()
    user_scores = {}
    for game in user_games:
        result = session.query(Result).join(Participant).filter(Participant.game_id == game.id, Participant.user_id == current_user.id).first()
        user_scores[game.name] = result.score if result else "No score yet"

    all_games = session.query(Game).all()
    available_games = [game for game in all_games if game not in user_games]

    return render_template("profile.html", user_scores=user_scores, available_games=available_games)

# Vista para el registro de nuevos usuarios
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["usuario"]
        email = request.form["email"]
        password = request.form["contraseña"]
        user = User(username=username, email=email)
        user.set_password(password)
        session.add(user)
        session.commit()
        return redirect(url_for("login"))
    else:
        return render_template("signup.html")

# Vista para iniciar sesión
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["contraseña"]
        user = session.query(User).filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for("home"))
        else:
            flash("Usuario o Contraseña incorrectos")
    return render_template("login.html")

# Vista para cerrar sesión
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

# Vista para la administración
@app.route("/admin", methods=["GET"])
@login_required
def admin():
    if not current_user.is_admin:
        return redirect(url_for("home"))
    users = session.query(User).all()
    games = session.query(Game).all()
    return render_template("admin.html", users=users, games=games)

# Promover un usuario a administrador
@app.route('/admin/promote', methods=['POST'])
@login_required
def promote_user():
    if not current_user.is_admin:
        return redirect(url_for("home"))

    username = request.form['username']
    user = session.query(User).filter_by(username=username).first()

    if user:
        user.is_admin = True
        session.commit()
        flash(f"User {username} has been promoted to admin.")
    else:
        flash(f"User {username} not found.")

    return redirect(url_for('admin'))

# Crear un nuevo usuario
@app.route('/admin/create_user', methods=['POST'])
@login_required
def create_user():
    if not current_user.is_admin:
        return redirect(url_for('home'))
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    user = User(username=username, email=email)
    user.set_password(password)
    session.add(user)
    session.commit()
    flash(f"User {username} created successfully.")
    return redirect(url_for('admin'))

# Editar un usuario existente
@app.route('/admin/edit_user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    if not current_user.is_admin:
        return redirect(url_for('home'))
    user = session.get(User, user_id)
    if request.method == 'POST':
        user.username = request.form['username']
        user.email = request.form['email']
        if 'password' in request.form and request.form['password']:
            user.set_password(request.form['password'])
        session.commit()
        flash(f"User {user.username} updated successfully.")
        return redirect(url_for('admin'))
    return render_template('edit_user.html', user=user)

# Eliminar un usuario
@app.route('/admin/delete_user/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    if not current_user.is_admin:
        return redirect(url_for('home'))
    user = session.get(User, user_id)
    session.delete(user)
    session.commit()
    flash(f"User {user.username} deleted successfully.")
    return redirect(url_for('admin'))

# Eliminar un participante
@app.route('/eliminate_player/<int:participant_id>', methods=['POST'])
@login_required
def eliminate_player(participant_id):
    participant = session.get(Participant, participant_id)
    if participant:
        session.delete(participant)
        session.commit()
        flash(f"Player {participant.user.username} has been eliminated.")
    else:
        flash("Participant not found.")
    return redirect(url_for('admin'))

# Crear un nuevo juego
@app.route('/admin/create_game', methods=['POST'])
@login_required
def create_game():
    if not current_user.is_admin:
        return redirect(url_for('home'))
    name = request.form['name']
    description = request.form['description']
    game = Game(name=name, description=description)
    session.add(game)
    session.commit()
    flash(f"Game {name} created successfully.")
    return redirect(url_for('admin'))

# Editar un juego existente
@app.route('/admin/edit_game/<int:game_id>', methods=['GET', 'POST'])
@login_required
def edit_game(game_id):
    if not current_user.is_admin:
        return redirect(url_for('home'))
    game = session.get(Game, game_id)
    if request.method == 'POST':
        game.name = request.form['name']
        game.description = request.form['description']
        session.commit()
        flash(f"Game {game.name} updated successfully.")
        return redirect(url_for('admin'))
    return render_template('edit_game.html', game=game)

# Eliminar un juego
@app.route('/admin/delete_game/<int:game_id>', methods=['POST'])
@login_required
def delete_game(game_id):
    if not current_user.is_admin:
        return redirect(url_for('home'))
    game = session.get(Game, game_id)
    session.delete(game)
    session.commit()
    flash(f"Game {game.name} deleted successfully.")
    return redirect(url_for('admin'))

# Vista para agregar resultados de un juego
@app.route('/game/<int:game_id>/results', methods=['GET', 'POST'])
@login_required
def game_results(game_id):
    game = session.get(Game, game_id)
    if request.method == 'POST':
        participant_id = request.form['participant_id']
        score = request.form['score']
        time = request.form['time']
        participant = session.get(Participant, participant_id)
        result = Result(participant_id=participant.id, score=score, time=time)
        session.add(result)
        session.commit()
        flash(f"Result for {participant.user.username} in {game.name} added successfully.")
        return redirect(url_for('game_results', game_id=game.id))
    results = session.query(Result).filter_by(participant_id=game.id).all()
    return render_template('results.html', game=game, results=results)

# Vista para mostrar estadísticas de un juego
@app.route('/game/<int:game_id>/stats')
def game_stats(game_id):
    game = session.get(Game, game_id)
    results = session.query(Result).join(Participant).filter(Participant.game_id == game_id).all()

    times = [result.time.total_seconds() for result in results]
    scores = [result.score for result in results]
    participants = [result.participant.user.username for result in results]

    plt.figure(figsize=(10, 6))
    plt.subplot(1, 2, 1)
    plt.barh(participants, times, color='skyblue')
    plt.xlabel('Time (seconds)')
    plt.title('Game Times')

    plt.subplot(1, 2, 2)
    plt.barh(participants, scores, color='orange')
    plt.xlabel('Scores')
    plt.title('Game Scores')

    plt.tight_layout()
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    return render_template('stats.html', plot_url=plot_url, game=game)

# Inscribir al usuario en un juego
@app.route("/signup_game", methods=["POST"])
@login_required
def signup_game():
    game_id = request.form["game_id"]
    game = session.get(Game, game_id)
    if game:
        participant = Participant(user_id=current_user.id, game_id=game.id, level="New")
        session.add(participant)
        session.commit()
        flash(f"You have successfully signed up for {game.name}!")
    else:
        flash("Game not found.")
    return redirect(url_for("home"))

# Vista para mostrar los rankings
@app.route('/rankings')
@login_required
def rankings():
    participants = session.query(Participant).all()
    rankings = sorted(participants, key=lambda p: (session.query(Result).filter_by(participant_id=p.id).first().score if session.query(Result).filter_by(participant_id=p.id).first() else 0), reverse=True)
    return render_template('rankings.html', rankings=rankings)

# Vista para mostrar los jugadores de League of Legends
@app.route('/league_of_legends')
def league_of_legends():
    game = session.query(Game).filter_by(name="League of Legends").first()
    results = session.query(Result).join(Participant).filter(Participant.game_id == game.id).order_by(Result.score.desc()).all()
    players = [{"name": result.participant.user.username, "score": result.score} for result in results]
    return render_template('league_of_legends.html', players=players)

# Vista para mostrar los jugadores de Dota 2
@app.route('/dota2')
def dota2():
    game = session.query(Game).filter_by(name="Dota 2").first()
    results = session.query(Result).join(Participant).filter(Participant.game_id == game.id).order_by(Result.score.desc()).all()
    players = [{"name": result.participant.user.username, "score": result.score} for result in results]
    return render_template('dota2.html', players=players)

# Vista para mostrar los jugadores de Counter-Strike: Global Offensive
@app.route('/csgo')
def csgo():
    game = session.query(Game).filter_by(name="Counter-Strike: Global Offensive").first()
    results = session.query(Result).join(Participant).filter(Participant.game_id == game.id).order_by(Result.score.desc()).all()
    players = [{"name": result.participant.user.username, "score": result.score} for result in results]
    return render_template('csgo.html', players=players)

if __name__ == "__main__":
    app.run(debug=True)  # Ejecuta la aplicación en modo de depuración