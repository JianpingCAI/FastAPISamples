from pydantic import BaseModel, EmailStr
from typing import List, Optional


class UserCreateDTO(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserResponseDTO(BaseModel):
    id: int
    username: str
    email: EmailStr
    blogs: Optional[List[int]]  # List of blog IDs

    class Config:
        from_attributes = True
