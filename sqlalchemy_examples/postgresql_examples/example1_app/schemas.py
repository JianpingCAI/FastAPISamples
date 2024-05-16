from typing import List, Optional
from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    name: str
    age: int


class UserCreate(UserBase):
    pass


# Model for email addresses
class EmailBase(BaseModel):
    email_address: str


class EmailCreate(EmailBase):
    pass


class Email(EmailBase):
    id: int
    user_id: Optional[int] = None
    model_config = ConfigDict(from_attributes=True)


# Model for reading user data, includes emails
class User(UserBase):
    id: int
    emails: List[Email] = []
    model_config = ConfigDict(from_attributes=True)
