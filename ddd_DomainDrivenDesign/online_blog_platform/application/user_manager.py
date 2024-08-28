from typing import Optional
from sqlalchemy.orm import Session
from domain.models.user import User
from domain.services.user_service import UserService


class UserManager:
    def __init__(self, db_session: Session):
        self.db_session = db_session
        self.user_service = UserService(db_session)

    def register_user(self, username: str, email: str, password: str) -> User:
        """
        This method handles the complete user registration process.
        It orchestrates the creation of the user and additional application logic.
        """
        user = self.user_service.create_user(username, email, password)

        # Application-specific logic can be added here, such as:
        # - Sending a welcome email
        # - Logging the registration event
        # - Publishing a domain event

        return user

    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        """
        This method handles user authentication, orchestrating domain services
        and applying application-specific logic.
        """
        user = self.user_service.authenticate_user(username, password)

        if user:
            # Application-specific logic, like updating last login time or
            # generating an authentication token, should be here.
            pass

        return user
