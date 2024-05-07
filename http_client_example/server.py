from fastapi import FastAPI
from pydantic import BaseModel
from models import *

app = FastAPI()


@app.post("/items/")
async def create_item(item: Item):
    item_data = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_data.update({"price_with_tax": price_with_tax})
    return item_data
