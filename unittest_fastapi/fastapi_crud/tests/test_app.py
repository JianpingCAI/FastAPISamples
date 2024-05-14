# tests/test_app.py
import os

os.environ["SKIP_TABLE_CREATION"] = "True"

import pytest

import sys

sys.path.append("..")
sys.path.append("../..")

from .conftest import create_test_database, client


# Example test class using asynchronous tests
@pytest.mark.usefixtures("create_test_database")
class TestCRUD:
    @pytest.mark.asyncio
    async def test_create_item(self, client):  # 'client' fixture is used here
        response = await client.post(
            "/items/", json={"name": "Test Item", "description": "A test item"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Test Item"
        assert "id" in data

    @pytest.mark.asyncio
    async def test_read_item(self, client):
        await client.post(
            "/items/", json={"name": "Test Item", "description": "A test item"}
        )
        response = await client.get("/items/1")
        assert response.status_code == 200
        assert response.json()["name"] == "Test Item"

    @pytest.mark.asyncio
    async def test_update_item(self, client):
        await client.post(
            "/items/",
            json={"name": "Original Item", "description": "An item to update"},
        )
        response = await client.put(
            "/items/1", json={"name": "Updated Item", "description": "An updated item"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Updated Item"

    @pytest.mark.asyncio
    async def test_delete_item(self, client):
        await client.post(
            "/items/",
            json={"name": "Item to Delete", "description": "This item will be deleted"},
        )
        response = await client.delete("/items/1")
        assert response.status_code == 200
        assert response.json()["name"] == "Item to Delete"
        assert response.json()["description"] == "This item will be deleted"
