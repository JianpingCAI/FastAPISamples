import asyncio
from typing import Dict
from fastapi import WebSocket
import websockets
import json
import subprocess


async def send_status_update(websocket: WebSocket, message: str) -> None:
    await websocket.send(json.dumps({"type": "status_update", "message": message}))


async def send_final_result(websocket, message):
    await websocket.send(json.dumps({"type": "final_result", "message": message}))


async def execute_task(websocket: WebSocket, task: Dict[str, str]) -> None:
    try:
        # Start the long-running shell script using subprocess
        process = subprocess.Popen(
            task["shell_script"],
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )

        # Stream output back to the server as status updates
        while True:
            output = process.stdout.readline()
            if output == "" and process.poll() is not None:
                break
            if output:
                await send_status_update(websocket, output.strip())

        # After finishing the task, send the final result
        retcode = process.poll()
        final_message = f"Task completed with exit code {retcode}"
        await send_final_result(websocket, final_message)
    except Exception as e:
        # Send error message back to the server
        await send_final_result(websocket, f"Failed to execute task due to: {str(e)}")


async def manage_tasks(websocket: WebSocket) -> None:
    try:
        await websocket.send(json.dumps({"type":"execute_task", "message": "Client connected"}))

        while True:
            message = await websocket.recv()
            data = json.loads(message)
            if data["type"] == "testrun":
                await execute_task(websocket, data)
    except json.JSONDecodeError:
        print("Failed to decode JSON from server.")
    except websockets.exceptions.ConnectionClosedError:
        print("WebSocket connection closed.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

async def connect_to_server(websocket: WebSocket) -> None:
    await websocket.send(json.dumps({"type":"connection", "message": "Client connected"}))
    message = await websocket.recv()
    print(f"Server message: {message}")
    
async def listen_for_tasks(uri: str, headers: str) -> None:
    while True:
        try:
            async with websockets.connect(uri, extra_headers=headers) as websocket:
                await connect_to_server(websocket)
                await manage_tasks(websocket)
        except websockets.exceptions.ConnectionClosedError:
            print("Connection lost... attempting to reconnect")
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            break  # Or continue based on your error handling policy


async def main():
    headers = {
        "Authorization": f"Bearer abc123"
    }  # This token must match one in your server's fake token DB
    uri = "ws://localhost:8000/ws/1"
    await listen_for_tasks(uri, headers)
    # await listen_for_tasks("ws://localhost:8000/ws/1")  # Example client ID: 1


if __name__ == "__main__":
    asyncio.run(main())
