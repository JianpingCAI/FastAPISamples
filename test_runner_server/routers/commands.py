from fastapi import APIRouter, HTTPException, WebSocket
from models import active_connections

router = APIRouter()


@router.post("/{runner_id}")
async def send_command(runner_id: int, command: str):
    websocket: WebSocket = active_connections.get(runner_id)
    if not websocket:
        raise HTTPException(status_code=404, detail="Runner not connected")
    await websocket.send_text(command)
    return {"message": "Command sent to runner"}
