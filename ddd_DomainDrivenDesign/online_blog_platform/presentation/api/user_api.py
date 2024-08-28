from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from domain.services.user_service import UserService
from infrastructure.database import get_db
from presentation.dto.user_dto import UserCreateDTO, UserResponseDTO

router = APIRouter()


@router.post("/users/", response_model=UserResponseDTO)
def create_user(user_dto: UserCreateDTO, db: Session = Depends(get_db)):
    user_service = UserService(db)
    user = user_service.create_user(
        user_dto.username, user_dto.email, user_dto.password
    )
    return user


@router.get("/users/{user_id}", response_model=UserResponseDTO)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user_service = UserService(db)
    user = user_service.get_user_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
