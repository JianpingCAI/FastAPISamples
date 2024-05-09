# OpenAPI Generator Tutorial for Generating Python Client SDK**

## Introduction

OpenAPI Generator is a tool that allows you to generate API client libraries, server stubs, and API documentation from OpenAPI Specifications. In this tutorial, we'll use it to generate a Python client SDK from a FastAPI server.

**Prerequisites:**

- Python 3.7+
- Node.js (Optional, required for easier installation)
- FastAPI
- OpenAPI Generator CLI

Let's break this tutorial into several steps:

## Part 1: Setting Up FastAPI and OpenAPI Documentation

1. **Install FastAPI and Uvicorn:**

    ```bash
    pip install fastapi uvicorn
    ```

2. **Create a Sample FastAPI Application:**

    Create a `main.py` file with the following content:

    ```python
    from fastapi import FastAPI
    from pydantic import BaseModel

    class Item(BaseModel):
        name: str
        description: str = None
        price: float
        tax: float = None

    app = FastAPI()

    @app.post("/items/", response_model=Item)
    async def create_item(item: Item):
        return item
    ```

3. **Run the FastAPI Application:**

    ```bash
    uvicorn main:app --reload
    ```

4. **Access the API Documentation:**

    - Open [http://localhost:8000/docs](http://localhost:8000/docs) to view the Swagger UI.
    - Open [http://localhost:8000/openapi.json](http://localhost:8000/openapi.json) to see the OpenAPI Specification in JSON format.

### Part 2: Installing and Setting Up OpenAPI Generator CLI

1. **Install OpenAPI Generator CLI:**

    - **Using Node Package Manager (NPM):**

      If you have Node.js and NPM installed, run:

      ```bash
      npm install @openapitools/openapi-generator-cli -g
      ```

    - **Manual Installation:**

      Download the JAR file directly:

      ```bash
      wget https://repo1.maven.org/maven2/org/openapitools/openapi-generator-cli/6.4.0/openapi-generator-cli-6.4.0.jar -O openapi-generator-cli.jar
      ```

      And alias the command:

      ```bash
      alias openapi-generator-cli='java -jar /path/to/openapi-generator-cli.jar'
      ```

2. **Verify Installation:**

    Run the following command:

    ```bash
    openapi-generator-cli version
    ```

    or if you downloaded the JAR file:

    ```bash
    java -jar openapi-generator-cli.jar version
    ```

    You should see the version number.

### Part 3: Generating Python Client SDK

1. **Generate the SDK:**

    - Navigate to the directory where your FastAPI app is running.

    - Run the following command:

    ```bash
    openapi-generator-cli generate -i http://localhost:8000/openapi.json -g python -o ./python-client
    ```

    - This command will use the OpenAPI specification available at `http://localhost:8000/openapi.json` and generate a Python client SDK inside the `python-client` directory.

### Part 4: Using the Generated Python Client SDK

1. **Install the Generated SDK:**

    ```bash
    pip install ./python-client
    ```

2. **Use the SDK in a Python Application:**

    ```python
    from python_client import ApiClient, Configuration
    from python_client.api import default_api
    from python_client.models import Item

    # Setup API Client
    config = Configuration(host="http://localhost:8000")
    client = ApiClient(configuration=config)
    api_instance = default_api.DefaultApi(api_client=client)

    # Create an Item
    item = Item(name="Sample Item", description="A sample item", price=100.0, tax=10.0)
    created_item = api_instance.create_item(item)

    print(f"Created Item: {created_item}")
    ```

### Summary

- We have successfully generated a Python client SDK from a FastAPI server using OpenAPI Generator.
- The SDK includes client classes and models that allow you to interact with the FastAPI server using Python.

**Further Steps:**

- Explore the OpenAPI Generator CLI to customize the output.
- Consider generating SDKs for other programming languages or for different APIs.

## dealing with multiple models and CRUD operations

When dealing with multiple models and CRUD operations in a FastAPI application, it's common to have endpoints with the same function names but different prefixes. OpenAPI Generator can handle this gracefully as it generates distinct API classes for each prefix.

In this tutorial, I'll guide you through handling this scenario step-by-step. Our goal is to generate a Python client SDK that maintains clear distinctions between the models and their CRUD operations.

### Part 1: Create a Complex FastAPI Application

1. **Install FastAPI and Uvicorn (if not already installed):**

    ```bash
    pip install fastapi uvicorn
    ```

2. **Create Models and Routers:**

    Let's assume we have two main models: `User` and `Item`. We'll create a separate router for each model with similar CRUD operation function names but different prefixes.

    **File Structure:**

    ```
    complex_fastapi_app/
    ├── main.py
    ├── models.py
    └── routers/
        ├── items.py
        └── users.py
    ```

3. **Create the `models.py` File:**

    This file will contain the Pydantic models for both `Item` and `User`.

    ```python
    # models.py
    from pydantic import BaseModel

    class Item(BaseModel):
        name: str
        description: str = None
        price: float
        tax: float = None

    class User(BaseModel):
        username: str
        email: str
        full_name: str = None
    ```

4. **Create the `items.py` Router:**

    Define the CRUD operations for the `Item` model in the `routers/items.py` file.

    ```python
    # routers/items.py
    from fastapi import APIRouter, HTTPException
    from models import Item

    router = APIRouter(
        prefix="/items",
        tags=["items"],
    )

    fake_items_db = {}

    @router.post("/", response_model=Item)
    async def create_item(item: Item):
        if item.name in fake_items_db:
            raise HTTPException(status_code=400, detail="Item already exists")
        fake_items_db[item.name] = item
        return item

    @router.get("/{item_name}", response_model=Item)
    async def read_item(item_name: str):
        item = fake_items_db.get(item_name)
        if item is None:
            raise HTTPException(status_code=404, detail="Item not found")
        return item
    ```

5. **Create the `users.py` Router:**

    Similarly, define the CRUD operations for the `User` model in the `routers/users.py` file.

    ```python
    # routers/users.py
    from fastapi import APIRouter, HTTPException
    from models import User

    router = APIRouter(
        prefix="/users",
        tags=["users"],
    )

    fake_users_db = {}

    @router.post("/", response_model=User)
    async def create_user(user: User):
        if user.username in fake_users_db:
            raise HTTPException(status_code=400, detail="User already exists")
        fake_users_db[user.username] = user
        return user

    @router.get("/{username}", response_model=User)
    async def read_user(username: str):
        user = fake_users_db.get(username)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    ```

6. **Create the `main.py` File:**

    Integrate both routers in the main FastAPI application.

    ```python
    # main.py
    from fastapi import FastAPI
    from routers import items, users

    app = FastAPI()

    app.include_router(items.router)
    app.include_router(users.router)
    ```

7. **Run the FastAPI Application:**

    ```bash
    uvicorn main:app --reload
    ```

8. **Verify the OpenAPI Documentation:**

    - Open [http://localhost:8000/docs](http://localhost:8000/docs) to view the Swagger UI.
    - Open [http://localhost:8000/openapi.json](http://localhost:8000/openapi.json) to see the OpenAPI Specification in JSON format.

### Part 2: Generate Python Client SDK with OpenAPI Generator

1. **Install OpenAPI Generator CLI:**

    If you haven't installed it yet, you can use the following method:

    - **Using Node Package Manager (NPM):**

      ```bash
      npm install @openapitools/openapi-generator-cli -g
      ```

    - **Manual Installation (JAR file):**

      ```bash
      wget https://repo1.maven.org/maven2/org/openapitools/openapi-generator-cli/6.4.0/openapi-generator-cli-6.4.0.jar -O openapi-generator-cli.jar
      ```

      Create an alias for easy usage:

      ```bash
      alias openapi-generator-cli='java -jar /path/to/openapi-generator-cli.jar'
      ```

2. **Generate the SDK:**

    - Navigate to the directory where your FastAPI app is running.

    - Run the following command:

    ```bash
    openapi-generator-cli generate -i http://localhost:8000/openapi.json -g python -o ./python-client
    ```

    - This command will use the OpenAPI specification available at `http://localhost:8000/openapi.json` and generate a Python client SDK inside the `python-client` directory.

### Part 3: Using the Generated Python Client SDK

1. **Install the Generated SDK:**

    ```bash
    pip install ./python-client
    ```

2. **Use the SDK in a Python Application:**

    ```python
    from python_client import ApiClient, Configuration
    from python_client.api import items_api, users_api
    from python_client.models import Item, User

    # Setup API Client
    config = Configuration(host="http://localhost:8000")
    client = ApiClient(configuration=config)

    # Item API Instance
    items_api_instance = items_api.ItemsApi(api_client=client)

    # User API Instance
    users_api_instance = users_api.UsersApi(api_client=client)

    # Create an Item
    item = Item(name="Sample Item", description="A sample item", price=100.0, tax=10.0)
    created_item = items_api_instance.create_item(item)

    print(f"Created Item: {created_item}")

    # Create a User
    user = User(username="johndoe", email="john@example.com", full_name="John Doe")
    created_user = users_api_instance.create_user(user)

    print(f"Created User: {created_user}")
    ```

### Summary

1. Create a FastAPI application with routers that use similar function names but different prefixes.
2. Use OpenAPI Generator to generate a Python client SDK.
3. Utilize the client SDK to interact with your FastAPI application.

## Jianping Notes

### Method3 - docker + jsonfile (I have used this method)

```bash
curl http://127.0.0.1:8000/openapi.json -o myapi.json

docker run --rm -v ${PWD}:/local openapitools/openapi-generator-cli generate -i /local/myapi.json -g python -o /local/myapi-client-sdk --additional-properties packageName=jianping_api_client

sudo chown -R cai: ./myapi-client-sdk

```

```bash

pip install ./myapi-client-sdk

```

### Method1 - docker + url

```bash

docker run --rm -v ${PWD}:/local openapitools/openapi-generator-cli generate -i http://localhost:8000/openapi.json -g python -o /local/myapi-client-sdk


```

### Method2 - cli + url

```bash

openapi-generator-cli generate -i http://localhost:8000/openapi.json -g python -o ./python-client

```

## Error with API not found

The error occurs because OpenAPI Generator relies on `operationId` fields in the OpenAPI specification to map endpoint functions to client methods. If the `operationId` is missing or improperly formatted, it might lead to incorrectly named client methods.

### Solution 1: Adding `operationId` to FastAPI Endpoints

In FastAPI, you can specify the `operation_id` directly in each route using the `operation_id` parameter.

1. **Update FastAPI Routes with `operationId`:**

    Update the `routers/items.py` and `routers/users.py` files to explicitly add the `operation_id` field.

    **`routers/items.py`:**

    ```python
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
    ```

    **`routers/users.py`:**

    ```python
    # routers/users.py
    from fastapi import APIRouter, HTTPException
    from models import User

    router = APIRouter(
        prefix="/users",
        tags=["users"],
    )

    fake_users_db = {}

    @router.post("/", response_model=User, operation_id="create_user")
    async def create_user(user: User):
        if user.username in fake_users_db:
            raise HTTPException(status_code=400, detail="User already exists")
        fake_users_db[user.username] = user
        return user

    @router.get("/{username}", response_model=User, operation_id="read_user")
    async def read_user(username: str):
        user = fake_users_db.get(username)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    ```

2. **Regenerate the Python Client SDK:**

    After adding `operation_id` to your FastAPI endpoints, regenerate the Python client SDK:

    ```bash
    openapi-generator-cli generate -i http://localhost:8000/openapi.json -g python -o ./python-client --additional-properties packageName=fastapi_client
    ```

3. **Install the Updated SDK:**

    Install the newly generated SDK:

    ```bash
    pip install ./python-client
    ```

4. **Use the SDK in Your Python Application:**

    Now, the client SDK methods will be correctly mapped to their corresponding endpoints:

    ```python
    from fastapi_client import ApiClient, Configuration
    from fastapi_client.api import items_api, users_api
    from fastapi_client.models import Item, User

    # Setup API Client
    config = Configuration(host="http://localhost:8000")
    client = ApiClient(configuration=config)

    # Item API Instance
    items_api_instance = items_api.ItemsApi(api_client=client)

    # User API Instance
    users_api_instance = users_api.UsersApi(api_client=client)

    # Create an Item
    item = Item(name="Sample Item", description="A sample item", price=100.0, tax=10.0)
    created_item = items_api_instance.create_item(item)

    print(f"Created Item: {created_item}")

    # Create a User
    user = User(username="johndoe", email="john@example.com", full_name="John Doe")
    created_user = users_api_instance.create_user(user)

    print(f"Created User: {created_user}")
    ```

### Solution 2: Avoiding Explicit `operationId` with Prefix Tags

If you prefer not to manually set `operation_id`, ensure each router uses distinct tags. In this scenario, OpenAPI Generator will differentiate the endpoints using the tags, making client method names unique.

1. **Ensure Unique Router Tags:**

    **`routers/items.py`:**

    ```python
    # routers/items.py
    from fastapi import APIRouter, HTTPException
    from models import Item

    router = APIRouter(
        prefix="/items",
        tags=["items"],  # Unique Tag
    )

    fake_items_db = {}

    @router.post("/", response_model=Item)
    async def create_item(item: Item):
        if item.name in fake_items_db:
            raise HTTPException(status_code=400, detail="Item already exists")
        fake_items_db[item.name] = item
        return item

    @router.get("/{item_name}", response_model=Item)
    async def read_item(item_name: str):
        item = fake_items_db.get(item_name)
        if item is None:
            raise HTTPException(status_code=404, detail="Item not found")
        return item
    ```

    **`routers/users.py`:**

    ```python
    # routers/users.py
    from fastapi import APIRouter, HTTPException
    from models import User

    router = APIRouter(
        prefix="/users",
        tags=["users"],  # Unique Tag
    )

    fake_users_db = {}

    @router.post("/", response_model=User)
    async def create_user(user: User):
        if user.username in fake_users_db:
            raise HTTPException(status_code=400, detail="User already exists")
        fake_users_db[user.username] = user
        return user

    @router.get("/{username}", response_model=User)
    async def read_user(username: str):
        user = fake_users_db.get(username)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    ```

2. **Regenerate the Python Client SDK:**

    Run the command again to regenerate the SDK:

    ```bash
    openapi-generator-cli generate -i http://localhost:8000/openapi.json -g python -o ./python-client --additional-properties packageName=fastapi_client
    ```

3. **Install the Updated SDK:**

    ```bash
    pip install ./python-client
    ```

### Conclusion

You can resolve the `AttributeError` by either explicitly defining `operation_id` for each FastAPI route or ensuring distinct tags across routers. Let me know if you need further clarification on any of the steps!
