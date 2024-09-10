from pydantic import BaseModel, ConfigDict
from typing import List, Optional


class BookBase(BaseModel):
    title: str


class BookCreate(BookBase):
    pass


class BookRead(BookBase):
    id: int
    authors: Optional[List["AuthorRead"]] = []

    class Config:
        orm_mode = True


class AuthorBase(BaseModel):
    name: str


class AuthorCreate(AuthorBase):
    pass


class AuthorRead(AuthorBase):
    id: int
    books: Optional[List[BookRead]] = []

    model_config = ConfigDict(from_attributes=True)
    # class Config:
    #     orm_mode = True
