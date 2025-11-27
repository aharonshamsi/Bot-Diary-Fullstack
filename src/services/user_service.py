from src.models.user_model import User
from src.repository.user_repo import insert_user

def create_user(data) -> User:

    try:
        username_str = str(data['username'])
        email_str = str(data['email'])
        password_str = str(data['password_hash'])

        new_user = User(
            username = username_str,
            email = email_str,
            password_hash = password_str
        )

    except ValueError:
        raise ValueError("Invalid user data: username, email or password_hash is missing or malformed")
    
    success = insert_user(new_user)

    if not success:
        raise ValueError("Failed to create user.")

    return new_user




