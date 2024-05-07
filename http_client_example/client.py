import httpx
from pydantic import ValidationError
from models import *


async def create_item(item: Item):
    url = "http://127.0.0.1:8000/items/"

    try:
        # Validate the item before sending
        item_data = item.dict()

        # Asynchronously send the POST request
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=item_data)

            # Raise an exception for unsuccessful requests
            response.raise_for_status()

            # Use Pydantic to parse and validate the response data
            response_item = ResponseItem(**response.json())
            return response_item

    except httpx.HTTPStatusError as http_error:
        # Handle HTTP errors
        print(f"HTTP error occurred: {http_error}")
    except ValidationError as val_error:
        # Handle validation errors
        print(f"Validation error for response data: {val_error}")
    except Exception as e:
        # Handle other potential errors
        print(f"An error occurred: {e}")


# Usage of the client function
import asyncio

item = Item(name="Sample Item", description="A test item", price=100.0, tax=10.0)


async def test():
    response_item = await create_item(item)
    if response_item:
        print(response_item)


asyncio.run(test())
