#Este archivo es usado para actualizar información de los usuarios, como promover a un usuario a administrador

from db import session
from models import User

def promote_to_admin(username):
    user = session.query(User).filter_by(username=username).first()
    if user:
        user.is_admin = True
        session.commit()
        print(f"User {username} has been promoted to admin.")
    else:
        print(f"User {username} not found.")

if __name__ == "__main__":
    promote_to_admin("admin")  # Reemplaza "admin" por el nombre de usuario real
