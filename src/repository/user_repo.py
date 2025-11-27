from app import db
from src.models.user_model import User


def insert_user(new_user: User) -> bool:
    try:
        db.session.add(new_user)
        db.session.commit()
        return True
    
    except Exception as e:
        db.session.rollback() # Cancels all actions that were entered
        return False
