from typing import Optional
from sqlalchemy.orm import Session
from .database import SessionLocal, engine, Base
from .models import Email, User
from .schemas import UserCreate


# Function to create a new user in the database
def create_user(db: Session, user: UserCreate):
    db_user = User(name=user.name, age=user.age)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_id: int, updated_data: UserCreate):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        db_user.name = updated_data.name
        db_user.age = updated_data.age
        db.commit()
        db.refresh(db_user)
        return db_user
    return None


def delete_user(db: Session, user_id: int):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
        return True
    return False


def add_email_to_user(db: Session, user_id: int, email: str):
    db_email = Email(email_address=email, user_id=user_id)
    db.add(db_email)
    db.commit()
    return db_email


# Function to get users by name
def get_user_by_name(db: Session, name: str) -> Optional[User]:
    return db.query(User).filter(User.name == name).first()


def get_user_by_id(db: Session, id: int) -> Optional[User]:
    return db.query(User).filter(User.id == id).first()
