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




def update_user_by_id(user_id: int, clean_data) -> bool:
    
    user = User.query.filter_by(user_id=user_id).first()

    if not user:
        return False

    if clean_data:
        if 'username' in clean_data:
            user.username = clean_data['username']

        if 'email' in clean_data:
            user.email = clean_data['email']

        if 'password_hash' in clean_data:
            user.password_hash = clean_data['password_hash']
        
        db.session.commit()
        return True
    
    return False


