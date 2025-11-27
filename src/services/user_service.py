from src.models.user_model import User
from src.repository.user_repo import insert_user
from src.repository.user_repo import delete_user_by_id
from src.repository.user_repo import update_user_by_id


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




def execute_deletion(user_id: str) -> None:
    
    try:
        user_id_int = int(user_id)

    except ValueError:
        raise ValueError("Invalid ID format provided.")
    
    success = delete_user_by_id(user_id_int)

    if not success:
        raise ValueError("Event not found or unauthorized for deletion.")
    

    

def execute_update(user_id: str, data) -> None:
    try:
        user_id_int = int(user_id)

        clean_data = {} # Create file json

        if 'username' in data:
            clean_data['username'] = str(data['username'])

        if 'email' in data:
            clean_data['email'] = str(data['email'])

        if 'password_hash' in data:
            clean_data['password_hash'] = str(data['password_hash'])

    except ValueError:
        raise ValueError("Invalid update data format")

    success = update_user_by_id(user_id_int, clean_data)

    if not success:
        raise ValueError("User not found or unauthorized for update.")




