from app import db
from sqlalchemy import func 
from src.models.user_model import User


def insert_user(new_user: User) -> bool:
    try:
        db.session.add(new_user)
        db.session.commit()
        return True
    
    except Exception as e:
        db.session.rollback() # Cancels all actions that were entered
        return False
    



def delete_user_by_id(user_id: int) -> bool:
    
    # ביצוע השאילתה מהדאטה ביס 
    user_to_delete = db.session.execute(
        db.select(User).filter_by(user_id=user_id)
    ).scalar_one_or_none()

    if user_to_delete:
        db.session.delete(user_to_delete)
        db.session.commit()
        return True
    
    return False

