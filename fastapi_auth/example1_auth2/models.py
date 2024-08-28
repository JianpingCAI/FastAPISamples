from pydantic import BaseModel
from typing import List, Optional


class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None
    role: Optional[str] = None
    hashed_password: Optional[str] = None  # Include hashed_password attribute


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
    scopes: List[str] = []


class RefreshTokenRequest(BaseModel):
    refresh_token: str
