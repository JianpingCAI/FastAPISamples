from fastapi import WebSocket, WebSocketDisconnect
from models import active_connections, Runner


async def websocket_endpoint(websocket: WebSocket, runner_id: int):
    await websocket.accept()
    active_connections[runner_id] = websocket
    try:
        while True:
            data = await websocket.receive_text()
            print(f"Received from runner {runner_id}: {data}")  # Log or process data
    except WebSocketDisconnect:
        active_connections.pop(runner_id, None)
        print(f"Runner {runner_id} disconnected")
