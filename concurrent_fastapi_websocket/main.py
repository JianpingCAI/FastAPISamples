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
        except (
            websockets.exceptions.InvalidURI,
            websockets.exceptions.InvalidHandshake,
            OSError,
        ) as e:
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
