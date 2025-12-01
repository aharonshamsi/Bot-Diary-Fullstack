
from src.models.user_model import User

def find_user_by_username(username: str) -> User:
    return User.query.filter_by(username=username).first()
