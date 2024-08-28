from typing import Optional
from sqlalchemy.orm import Session
from infrastructure.orm.user_mapper import UserORM
from domain.models.user import User


class UserRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def save(self, user: User) -> None:
        user_orm = UserORM(
            username=user.username, email=user.email, password=user.password
        )
        self.db_session.add(user_orm)
        self.db_session.commit()

    def find_by_id(self, user_id: int) -> Optional[User]:
        user_orm = self.db_session.query(UserORM).filter(UserORM.id == user_id).first()
        if user_orm:
            return User(
                id=user_orm.id,
                username=user_orm.username,
                email=user_orm.email,
                password=user_orm.password,
            )
        return None

    def find_by_username(self, username: str) -> Optional[User]:
        user_orm = (
            self.db_session.query(UserORM).filter(UserORM.username == username).first()
        )
        if user_orm:
            return User(
                id=user_orm.id,
                username=user_orm.username,
                email=user_orm.email,
                password=user_orm.password,
            )
        return None
