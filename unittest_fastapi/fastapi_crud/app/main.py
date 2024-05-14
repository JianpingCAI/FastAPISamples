# app/main.py
from typing import List
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import NoResultFound

from .db_init import create_tables

from . import models, schemas
from .database import get_db_session
import os

app = FastAPI()

# Create database tables
if os.getenv("SKIP_TABLE_CREATION") != "True":
    app.add_event_handler("startup", create_tables)
# app.add_event_handler("startup", create_tables)
# @app.on_event("startup")
# async def startup_event():
#     create_tables()


@app.post("/items/", response_model=schemas.Item)
async def create_item(
    item: schemas.ItemCreate, db: AsyncSession = Depends(get_db_session)
):
    new_item = models.Item(**item.dict())
    db.add(new_item)
    await db.commit()
    await db.refresh(new_item)
    return new_item


@app.get("/items/", response_model=List[schemas.Item])
async def read_items(db: AsyncSession = Depends(get_db_session)):
    async with db:
        result = await db.execute(select(models.Item))
        items = result.scalars().all()
    return items


@app.get("/items/{item_id}", response_model=schemas.Item)
async def read_item(item_id: int, db: AsyncSession = Depends(get_db_session)):
    async with db:
        try:
            result = await db.execute(
                select(models.Item).filter(models.Item.id == item_id)
            )
            item = result.scalars().one()
        except NoResultFound:
            raise HTTPException(status_code=404, detail="Item not found")
    return item


@app.put("/items/{item_id}", response_model=schemas.Item)
async def update_item(
    item_id: int,
    item_data: schemas.ItemCreate,
    db: AsyncSession = Depends(get_db_session),
):
    async with db:
        try:
            result = await db.execute(
                select(models.Item).filter(models.Item.id == item_id)
            )
            item = result.scalars().one()
        except NoResultFound:
            raise HTTPException(status_code=404, detail="Item not found")

        item_data_dict = item_data.dict(exclude_unset=True)
        for key, value in item_data_dict.items():
            setattr(item, key, value)

        await db.commit()
        await db.refresh(item)
    return item


@app.delete("/items/{item_id}", response_model=schemas.Item)
async def delete_item(item_id: int, db: AsyncSession = Depends(get_db_session)):
    async with db:
        try:
            result = await db.execute(
                select(models.Item).filter(models.Item.id == item_id)
            )
            item = result.scalars().one()
        except NoResultFound:
            raise HTTPException(status_code=404, detail="Item not found")

        await db.delete(item)
        await db.commit()
    return item
