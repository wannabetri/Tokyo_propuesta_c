#Este archivo define los modelos de la base de datos usando SQLAlchemy. Incluye las clases User, Game, Participant y Result.

from datetime import timedelta  # Importa timedelta para manejar intervalos de tiempo
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Text, Interval  # Importa elementos necesarios de SQLAlchemy para definir modelos
from sqlalchemy.orm import relationship  # Importa la relación entre modelos
from sqlalchemy.ext.declarative import declarative_base  # Importa la clase base declarativa
from werkzeug.security import generate_password_hash, check_password_hash  # Importa funciones para trabajar con contraseñas seguras
from flask_login import UserMixin  # Importa UserMixin para la gestión de usuarios en Flask

Base = declarative_base()  # Crea una instancia de la clase base declarativa de SQLAlchemy

class User(Base, UserMixin):  # Define el modelo de usuario, heredando de Base y UserMixin
    __tablename__ = "users"  # Nombre de la tabla en la base de datos

    # Definición de atributos del usuario
    id = Column(Integer, primary_key=True)  # Identificador único del usuario
    username = Column(String(50), unique=True, nullable=False)  # Nombre de usuario único y obligatorio
    email = Column(String(120), unique=True, nullable=False)  # Correo electrónico único y obligatorio
    password_hash = Column(String(128), nullable=False)  # Hash de la contraseña del usuario
    is_admin = Column(Boolean, default=False)  # Indica si el usuario es administrador o no

    participants = relationship("Participant", back_populates="user")  # Relación con los participantes en juegos

    def set_password(self, password):  # Método para establecer la contraseña del usuario
        self.password_hash = generate_password_hash(password)  # Genera un hash seguro para la contraseña

    def check_password(self, password):  # Método para verificar la contraseña del usuario
        return check_password_hash(self.password_hash, password)  # Comprueba si la contraseña coincide con el hash almacenado

class Game(Base):  # Define el modelo de juego
    __tablename__ = 'games'  # Nombre de la tabla en la base de datos
    id = Column(Integer, primary_key=True)  # Identificador único del juego
    name = Column(String(100), nullable=False)  # Nombre del juego
    description = Column(Text)  # Descripción del juego

    participants = relationship("Participant", back_populates="game")  # Relación con los participantes en el juego

class Participant(Base):  # Define el modelo de participante en un juego
    __tablename__ = 'participants'  # Nombre de la tabla en la base de datos
    id = Column(Integer, primary_key=True)  # Identificador único del participante
    user_id = Column(Integer, ForeignKey('users.id'))  # ID del usuario participante
    game_id = Column(Integer, ForeignKey('games.id'))  # ID del juego en el que participa el usuario
    level = Column(String(7))  # Nivel del participante en el juego

    user = relationship("User", back_populates="participants")  # Relación con el usuario participante
    game = relationship("Game", back_populates="participants")  # Relación con el juego en el que participa
    results = relationship("Result", back_populates="participant")  # Asegúrar que esta relación esté definida
class Result(Base):  # Define el modelo de resultado en un juego
    __tablename__ = 'results'  # Nombre de la tabla en la base de datos
    id = Column(Integer, primary_key=True)  # Identificador único del resultado
    participant_id = Column(Integer, ForeignKey('participants.id'))  # ID del participante asociado al resultado
    score = Column(Integer)  # Puntuación obtenida por el participante
    time = Column(Interval, default=timedelta)  # Tiempo que duró la partida

    participant = relationship("Participant", back_populates="results")  # Relación con el participante asociado al resultado

#Asegúrar que todas las relaciones estén correctamente definidas
Participant.results = relationship("Result", order_by=Result.id, back_populates="participant")