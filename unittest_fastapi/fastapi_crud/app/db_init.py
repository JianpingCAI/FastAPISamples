# app/db_init.py
from .database import engine
from .models import Base


# Define a function to create database tables
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
