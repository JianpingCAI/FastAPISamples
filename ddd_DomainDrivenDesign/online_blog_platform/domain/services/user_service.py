from typing import Optional
from domain.models.user import User
from domain.repositories.user_repository import UserRepository

class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def create_user(self, username: str, email: str, password: str) -> User:
        user = User(username=username, email=email, password=password)
        self.user_repository.save(user)
        return user

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        return self.user_repository.find_by_id(user_id)

    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        user = self.user_repository.find_by_username(username)
        if user and user.password == password:
            return user
        return None
