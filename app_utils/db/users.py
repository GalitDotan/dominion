# Mock database
from app_utils.app_utils import verify_password
from app_utils.models.app_models import User

_users_db = {
    "user1": {
        "username": "user1",
        "hashed_password": "$2b$12$9I8HKekS6nYDAt9UxDuUWOnYFrf8tVlQwvH8tKaeI0V/Bq3X4KxJy",
        # Hashed version of "password"
    }
}


def get_user(username: str):
    if username in _users_db:
        user_dict = _users_db[username]
        return User(**user_dict)


def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user or not verify_password(password, user.hashed_password):
        return False
    return user
