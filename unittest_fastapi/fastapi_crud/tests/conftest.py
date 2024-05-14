# tests/test_app.py
import os

os.environ["SKIP_TABLE_CREATION"] = "True"

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

import sys

sys.path.append("..")
sys.path.append("../..")
from fastapi_crud.app.main import app
from fastapi_crud.app.models import Base
from fastapi_crud.app.database import get_db_session


# Configuration for an in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

# Setup the testing database engine and session
engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
)


# Fixture to create and drop the database tables
# Ensure this fixture correctly sets up the database and manages transactions
@pytest.fixture(scope="function", autouse=True)
async def create_test_database():

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    try:
        yield  # This ensures that the test runs with the database setup
    finally:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)


# This fixture creates the test client and overrides the session dependency
@pytest.fixture
async def client():
    # Define a dependency override for the database session
    async def override_get_db():
        async with TestingSessionLocal() as session:
            yield session

    # Apply the dependency override
    app.dependency_overrides[get_db_session] = override_get_db

    # Use AsyncClient for testing
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

    # Clear overrides after the test
    app.dependency_overrides.clear()
