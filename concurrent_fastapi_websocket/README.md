### Part 1: Setting Up the FastAPI Application

In this tutorial, we'll build a FastAPI application that serves HTTP requests and acts as a WebSocket client. We'll handle both functionalities concurrently while ensuring proper error handling and graceful shutdown.

#### Step 1: Install Required Libraries

First, ensure you have the necessary libraries installed. Open your terminal and run:

```bash
pip install fastapi uvicorn websockets
```

#### Step 2: Create the FastAPI Application

Create a Python file (e.g., `main.py`) and start by importing the required modules and setting up a simple FastAPI application:

```python
import asyncio
import uvicorn
from fastapi import FastAPI
import websockets

app = FastAPI()

# Define a simple API endpoint
@app.get("/")
async def read_root():
    return {"message": "Hello World"}
```

In this snippet:

- We import `asyncio`, `uvicorn`, `FastAPI`, and `websockets`.
- We create an instance of the FastAPI application.
- We define a simple API endpoint that returns a "Hello World" message.

Next, we'll add the WebSocket client functionality and ensure it runs concurrently with the FastAPI server.

### Part 2: Implementing the WebSocket Client

#### Step 3: Define the WebSocket Client

Add an asynchronous function to handle the WebSocket client connection. This function will attempt to connect to a WebSocket server and listen for messages:

```python
async def websocket_client():
    uri = "ws://localhost:8001"  # Change this to the address of your WebSocket server
    while True:
        try:
            async with websockets.connect(uri) as websocket:
                try:
                    while True:
                        message = await websocket.recv()
                        print(f"Received message from WebSocket server: {message}")
                except websockets.exceptions.ConnectionClosedError:
                    print("WebSocket connection closed, attempting to reconnect...")
                    await asyncio.sleep(5)  # Wait before attempting to reconnect
        except (websockets.exceptions.InvalidURI, websockets.exceptions.InvalidHandshake, OSError) as e:
            print(f"Failed to connect to WebSocket server: {e}")
            await asyncio.sleep(5)  # Wait before attempting to reconnect
```

In this function:

- We define the WebSocket server URI.
- We use an infinite loop to continuously attempt to connect to the WebSocket server.
- If the connection is established, we listen for messages and print them.
- If the connection is closed or fails, we handle the exception and wait 5 seconds before retrying.

Next, we'll integrate this WebSocket client with the FastAPI application's lifecycle using the `asynccontextmanager`.

### Part 3: Using `asynccontextmanager` for Lifespan Management

#### Step 4: Understand `asynccontextmanager`

The `asynccontextmanager` is a convenient way to manage the lifespan of asynchronous tasks in Python. It allows us to define setup and teardown code that runs at the start and end of a context.

Here's a simple example to illustrate how `asynccontextmanager` works:

```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan_example():
    print("Setup")
    yield
    print("Teardown")

async def main():
    async with lifespan_example():
        print("Running")

# Running the main function will print:
# Setup
# Running
# Teardown

asyncio.run(main())
```

In this example:

- `lifespan_example` is an asynchronous context manager that prints "Setup" when entered and "Teardown" when exited.
- The `yield` statement marks the point where the context is active.

Next, we'll apply this concept to our FastAPI application to manage the WebSocket client.

### Part 4: Integrating the WebSocket Client with FastAPI Lifespan

#### Step 5: Define the Lifespan Context Manager

We'll use the `asynccontextmanager` to start the WebSocket client when the FastAPI application starts and stop it when the application shuts down:

```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Start the WebSocket client in the background
    task = asyncio.create_task(websocket_client())
    try:
        yield
    finally:
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            print("WebSocket client task cancelled.")
```

In this context manager:

- We create a background task to run the WebSocket client.
- We use `yield` to allow the FastAPI application to run.
- We cancel the WebSocket client task and handle any cancellation errors during the shutdown process.

#### Step 6: Set the Lifespan Context in FastAPI

Finally, integrate the lifespan context manager into the FastAPI application:

```python
app.router.lifespan_context = lifespan
```

This line sets the `lifespan_context` attribute of the FastAPI router to the custom `lifespan` context manager.

### Part 5: Running the Application

#### Step 7: Start the FastAPI Application

Add the code to run the FastAPI application using `uvicorn`:

```python
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### Complete Code

Here is the complete code with all the steps integrated:

```python
import asyncio
import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager
import websockets

app = FastAPI()

# Define a simple API endpoint
@app.get("/")
async def read_root():
    return {"message": "Hello World"}

async def websocket_client():
    uri = "ws://localhost:8001"  # Change this to the address of your WebSocket server
    while True:
        try:
            async with websockets.connect(uri) as websocket:
                try:
                    while True:
                        message = await websocket.recv()
                        print(f"Received message from WebSocket server: {message}")
                except websockets.exceptions.ConnectionClosedError:
                    print("WebSocket connection closed, attempting to reconnect...")
                    await asyncio.sleep(5)  # Wait before attempting to reconnect
        except (websockets.exceptions.InvalidURI, websockets.exceptions.InvalidHandshake, OSError) as e:
            print(f"Failed to connect to WebSocket server: {e}")
            await asyncio.sleep(5)  # Wait before attempting to reconnect

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Start the WebSocket client in the background
    task = asyncio.create_task(websocket_client())
    try:
        yield
    finally:
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            print("WebSocket client task cancelled.")

app.router.lifespan_context = lifespan

if __name__ == "__main__":
    # Run the FastAPI server
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### Summary

In this tutorial, we created a FastAPI application that concurrently runs as a WebSocket client. We used the `asynccontextmanager` to manage the lifespan of the WebSocket client, ensuring it starts and stops correctly with the FastAPI application. This setup allows the FastAPI application to handle HTTP requests and WebSocket communications efficiently.

To support multiple WebSocket clients, you can extend the implementation to manage a list of WebSocket URIs and create a separate task for each WebSocket client connection. We'll modify the lifespan context manager to start multiple WebSocket client tasks and handle their shutdown appropriately.

### Updated Implementation

#### Step 1: Define Multiple WebSocket URIs

First, define a list of WebSocket server URIs to which you want to connect:

```python
websocket_uris = [
    "ws://localhost:8001",
    "ws://localhost:8002",
    "ws://localhost:8003"  # Add more URIs as needed
]
```

#### Step 2: Modify the WebSocket Client Function

Update the `websocket_client` function to accept a URI parameter:

```python
async def websocket_client(uri: str):
    while True:
        try:
            async with websockets.connect(uri) as websocket:
                try:
                    while True:
                        message = await websocket.recv()
                        print(f"Received message from WebSocket server at {uri}: {message}")
                except websockets.exceptions.ConnectionClosedError:
                    print(f"WebSocket connection to {uri} closed, attempting to reconnect...")
                    await asyncio.sleep(5)  # Wait before attempting to reconnect
        except (websockets.exceptions.InvalidURI, websockets.exceptions.InvalidHandshake, OSError) as e:
            print(f"Failed to connect to WebSocket server at {uri}: {e}")
            await asyncio.sleep(5)  # Wait before attempting to reconnect
```

#### Step 3: Start Multiple WebSocket Client Tasks

Modify the lifespan context manager to start a WebSocket client task for each URI:

```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    tasks = []
    for uri in websocket_uris:
        task = asyncio.create_task(websocket_client(uri))
        tasks.append(task)
    try:
        yield
    finally:
        for task in tasks:
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                print("WebSocket client task cancelled.")
```

In this context manager:

- We create a list of tasks, each corresponding to a WebSocket client connection.
- Each task runs the `websocket_client` function with a different URI.
- During shutdown, all tasks are cancelled gracefully.

#### Step 4: Set the Lifespan Context in FastAPI

Set the `lifespan_context` attribute of the FastAPI router to the custom `lifespan` context manager:

```python
app.router.lifespan_context = lifespan
```

### Complete Updated Code

Here is the complete code with support for multiple WebSocket clients:

```python
import asyncio
import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager
import websockets

app = FastAPI()

# Define a list of WebSocket server URIs
websocket_uris = [
    "ws://localhost:8001",
    "ws://localhost:8002",
    "ws://localhost:8003"  # Add more URIs as needed
]

# Define a simple API endpoint
@app.get("/")
async def read_root():
    return {"message": "Hello World"}

async def websocket_client(uri: str):
    while True:
        try:
            async with websockets.connect(uri) as websocket:
                try:
                    while True:
                        message = await websocket.recv()
                        print(f"Received message from WebSocket server at {uri}: {message}")
                except websockets.exceptions.ConnectionClosedError:
                    print(f"WebSocket connection to {uri} closed, attempting to reconnect...")
                    await asyncio.sleep(5)  # Wait before attempting to reconnect
        except (websockets.exceptions.InvalidURI, websockets.exceptions.InvalidHandshake, OSError) as e:
            print(f"Failed to connect to WebSocket server at {uri}: {e}")
            await asyncio.sleep(5)  # Wait before attempting to reconnect

@asynccontextmanager
async def lifespan(app: FastAPI):
    tasks = []
    for uri in websocket_uris:
        task = asyncio.create_task(websocket_client(uri))
        tasks.append(task)
    try:
        yield
    finally:
        for task in tasks:
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                print("WebSocket client task cancelled.")

app.router.lifespan_context = lifespan

if __name__ == "__main__":
    # Run the FastAPI server
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### Summary

In this updated implementation, we extended the FastAPI application to support multiple WebSocket clients. Each client connects to a different WebSocket server URI, and all connections are managed concurrently. The `asynccontextmanager` ensures that all WebSocket client tasks are started during the application startup and cancelled gracefully during the shutdown. This setup allows the FastAPI application to handle HTTP requests while maintaining multiple WebSocket connections efficiently.
