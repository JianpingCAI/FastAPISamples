from pydantic import BaseModel
from typing import List, Optional


class OrderBase(BaseModel):
    name: str
    customer_id: str
    product_id: str


class OrderCreate(OrderBase):
    pass


class OrderUpdate(OrderBase):
    pass


class OrderInDB(OrderBase):
    id: str

    class Config:
        from_attributes = True


class CustomerBase(BaseModel):
    customer_name: str


class CustomerCreate(CustomerBase):
    pass


class CustomerInDB(CustomerBase):
    id: str
    orders: List[OrderInDB] = []

    class Config:
        from_attributes = True


class ProductBase(BaseModel):
    product_name: str


class ProductCreate(ProductBase):
    pass


class ProductInDB(ProductBase):
    id: str
    orders: List[OrderInDB] = []

    class Config:
        from_attributes = True
