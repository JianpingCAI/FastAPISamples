# # app/database.py
# from sqlalchemy import create_engine, Column, Integer, String
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.future import select

# SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./test.db"

# engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True, future=True)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)

# Base = declarative_base()


# def get_db_session():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./test.db"

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)

# Create a custom session class that can be used for async operations
AsyncSessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

from sqlalchemy.orm import declarative_base
Base = declarative_base()


async def get_db_session():
    async with AsyncSessionLocal() as session:
        yield session
