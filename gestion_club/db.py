#Este archivo configura la conexión a la base de datos y crea una sesión para interactuar con ella.

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

# Crea el engine para la base de datos
engine = create_engine('sqlite:///database/gestion.db',
                       connect_args={"check_same_thread": False})

# Crea las tablas en la base de datos
Base.metadata.create_all(engine)

# Configura la sesión
Session = sessionmaker(bind=engine)
session = Session()