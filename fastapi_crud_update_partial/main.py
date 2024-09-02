import os
from typing import List, Optional

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel, ConfigDict

# Define the database URL
DATABASE_URL = "sqlite:///./test.db"

# If the database file exists and you want to recreate it, remove the file
if os.path.exists("test.db"):
    os.remove("test.db")

# SQLAlchemy setup
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}, echo=True
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, unique=True, nullable=True, index=True)
    address = Column(String, nullable=True, index=True)


# Create the database and table
Base.metadata.create_all(bind=engine)


# Pydantic models
class UserBase(BaseModel):
    username: str
    email: str
    address: Optional[str] = None


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None


class UserResponse(UserBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

    # class Config:
    #     from_attributes = True


# FastAPI setup
app = FastAPI()


# Dependency to get the DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# CRUD Operations


# Create a new user
@app.post("/users/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = User(**user.model_dump())
    db.add(new_user)
    db.commit()
    # db.refresh(new_user)
    return new_user


# Read all users
@app.get("/users/", response_model=List[UserResponse])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = db.query(User).offset(skip).limit(limit).all()
    return users


# Read a user by ID
@app.get("/users/{user_id}", response_model=UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# Update a user
@app.put("/users/{user_id}", response_model=UserResponse)
def update_user_endpoint(
    user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)
):
    updated_user = update_user(db, user_id, user_update)
    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user


def update_user(
    db: Session, user_id: int, user_update: UserUpdate
) -> Optional[UserResponse]:
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        return None

    # Update user fields based on provided values, allowing setting to None
    update_data = user_update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_user, key, value)

    db.commit()
    # db.refresh(db_user)
    return db_user


# Delete a user
@app.delete("/users/{user_id}", response_model=UserResponse)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return user


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
