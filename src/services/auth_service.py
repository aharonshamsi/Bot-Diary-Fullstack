
from src.repository.auth_repo import find_user_by_username
from werkzeug.security import check_password_hash


def authenticate_user(username: str, password: str):
    
    user = find_user_by_username(username)

    if not user:
        raise ValueError("Invalid username or password")

    if not check_password_hash(user.password_hash, password):
        raise ValueError("Invalid username or password")
    
    return user


