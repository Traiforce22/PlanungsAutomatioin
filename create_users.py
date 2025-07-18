from db.session import SessionLocal
from db.models import User
from utils.auth import hash_password

def create_user(username: str, password: str, role: str = "user"):
    db = SessionLocal()
    hashed_pw = hash_password(password)
    user = User(username=username, password_hash=hashed_pw, role=role)
    db.add(user)
    db.commit()
    db.close()

if __name__ == "__main__":
    create_user("Marco", "Chef", "admin")
    create_user("Mitarbeiter", "Hello", "user")
