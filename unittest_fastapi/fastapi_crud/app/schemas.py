# app/schemas.py
from pydantic import BaseModel, ConfigDict
from typing import Optional


class ItemBase(BaseModel):
    name: str
    description: Optional[str] = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int

    # class Config:
    #     from_attributes = True
    model_config = ConfigDict(from_attributes=True)
