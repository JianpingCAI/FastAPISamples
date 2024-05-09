# routers/items.py
from fastapi import APIRouter, HTTPException
from models import Item

router = APIRouter(
    prefix="/items",
    tags=["items"],
)

fake_items_db = {}


@router.post("/", response_model=Item, operation_id="create_item")
async def create_item(item: Item):
    if item.name in fake_items_db:
        raise HTTPException(status_code=400, detail="Item already exists")
    fake_items_db[item.name] = item
    return item


@router.get("/{item_name}", response_model=Item, operation_id="read_item")
async def read_item(item_name: str):
    item = fake_items_db.get(item_name)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item
