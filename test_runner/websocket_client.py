# websocket_client.py
from command_handler import handle_command
import websockets
import asyncio
from utils import log_info, log_error
from config import config


async def start_websocket_client(runner_id):
    uri = f"{config.websocket_url}/{runner_id}"
    while True:
        try:
            async with websockets.connect(uri) as websocket:
                await websocket.send("Runner connected")
                await listen_to_messages(websocket)
        except websockets.exceptions.ConnectionClosed:
            log_error("WebSocket connection closed, retrying...")
            await asyncio.sleep(10)  # wait before reconnecting


async def listen_to_messages(websocket):
    try:
        async for message in websocket:
            handle_command(message)
    except Exception as e:
        log_error(f"Error in message handling: {e}")
