from pydantic import BaseModel


class Item(BaseModel):
    name: str
    description: str
    price: float
    tax: float


class ResponseItem(BaseModel):
    name: str
    description: str
    price: float
    tax: float
    price_with_tax: float
