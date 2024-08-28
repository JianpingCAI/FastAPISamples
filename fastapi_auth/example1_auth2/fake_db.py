from utils import get_password_hash


fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": get_password_hash("secret"),  # bcrypt hash for "secret"
        "disabled": False,
        "role": "admin",
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderland",
        "email": "alice@example.com",
        "hashed_password": get_password_hash("secret"),  # bcrypt hash for "secret"
        "disabled": False,
        "role": "user",
    },
}


# A separate dictionary to store refresh tokens
fake_refresh_tokens = {}
