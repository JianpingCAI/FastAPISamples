# app/main.py
from typing import List
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from . import models, schemas
from .database import get_db_session
from .models import Item

app = FastAPI()


@app.post("/items/", response_model=schemas.Item)
async def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db_session)):
    db_item = models.Item(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


@app.get("/items/", response_model=List[schemas.Item])
async def read_items(db: Session = Depends(get_db_session)):
    items = db.execute(select(models.Item)).scalars().all()
    return items


@app.get("/items/{item_id}", response_model=schemas.Item)
async def read_item(item_id: int, db: Session = Depends(get_db_session)):
    item = (
        db.execute(select(models.Item).filter(models.Item.id == item_id))
        .scalars()
        .first()
    )
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@app.put("/items/{item_id}", response_model=schemas.Item)
async def update_item(
    item_id: int,
    updated_item: schemas.ItemCreate,
    db: Session = Depends(get_db_session),
):
    db_item = (
        db.execute(select(models.Item).filter(models.Item.id == item_id))
        .scalars()
        .first()
    )
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    for var, value in vars(updated_item).items():
        setattr(db_item, var, value)
    db.commit()
    return db_item


@app.delete("/items/{item_id}", response_model=schemas.Item)
async def delete_item(item_id: int, db: Session = Depends(get_db_session)):
    db_item = (
        db.execute(select(models.Item).filter(models.Item.id == item_id))
        .scalars()
        .first()
    )
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(db_item)
    db.commit()
    return db_item
