from fastapi import (
    FastAPI,
    HTTPException,
    WebSocket,
    WebSocketDisconnect,
    Depends,
    status,
)
from fastapi.security import OAuth2PasswordBearer
import json
from typing import Dict, List, Tuple
from config import settings
from models import Task
from database import SessionLocal, TaskModel


app = FastAPI(title=settings.app_name)


class ConnectionManager:
    def __init__(self) -> None:
        # Maps client IDs to their WebSocket connections
        self.active_connections: Dict[int, WebSocket] = {}

    async def connect(self, client_id: int, websocket: WebSocket) -> None:
        await websocket.accept()
        self.active_connections[client_id] = websocket
        print(f"Client {client_id} connected.")

    def disconnect(self, client_id: int) -> None:
        if client_id in self.active_connections:
            del self.active_connections[client_id]
            print(f"Client {client_id} disconnected.")

    async def send_task(self, client_id: int, message: str) -> None:
        if client_id in self.active_connections:
            await self.active_connections[client_id].send_text(message)
            print(f"Sent message to Client {client_id}.")
        else:
            print(f"Client {client_id} not found, cannot send message.")

    async def broadcast(self, message: str) -> None:
        for client_id, websocket in self.active_connections.items():
            await websocket.send_text(message)
            print(f"Broadcasted message to Client {client_id}.")


manager = ConnectionManager()


def parse_auth_header(headers: List[Tuple[bytes, bytes]]) -> str:
    for name, value in headers:
        # Ensure name and value are treated as strings
        name_str = name.decode() if isinstance(name, bytes) else name
        value_str = value.decode() if isinstance(value, bytes) else value

        if name_str.lower() == "authorization":
            if value_str.startswith("Bearer "):
                return value_str[7:]  # Extract token after "Bearer "
    return ""


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Fake database of tokens for demonstration purposes
fake_token_db = {"abc123": {"user_id": "user1"}}


async def get_current_user(token: str) -> dict:

    if token and token in fake_token_db:
        return fake_token_db[token]
    else:
        return None


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    # Ensure the client is connected
    await manager.connect(websocket)

    token = parse_auth_header(websocket.headers.items())

    if not token:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )

    user = await get_current_user(token)
    if not user:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )
    print(f"from user: {user['user_id']}")

    try:
        # Loop to keep the connection open and handle messages
        while True:
            data = await websocket.receive_text()
            data_json = json.loads(data)

            # Handling different types of messages
            if data_json["type"] == "execute_task":
                # Send a task to the client (task details are pre-defined or could be dynamic)
                task = Task(
                    type="testrun",
                    name="Data Analysis",
                    description="Analyze the provided data set.",
                    shell_script="analyze.sh",
                )
                await manager.send_task(task.json(), websocket)

            elif data_json["type"] == "status_update":
                # Process real-time status updates from the client
                print(f"Client {client_id} status update: {data_json['message']}")
                # Optionally, update task status in the database or internal state
                update_task_status(client_id, "running", data_json["message"])

            elif data_json["type"] == "final_result":
                # Handle the final result message from the client
                print(f"Client {client_id} final result: {data_json['message']}")
                # Update the task as completed in the database or internal state
                update_task_status(client_id, "completed", data_json["message"])

            elif data_json["type"] == "connect":
                # Handle client connection
                print(f"Client {client_id} connected")

            elif data_json["type"] == "disconnect":
                # Handle client disconnection
                manager.disconnect(websocket)
                print(f"Client {client_id} disconnected")
                break

    except WebSocketDisconnect:
        # Handle client disconnection
        manager.disconnect(websocket)
        print(f"Client {client_id} disconnected")
        # Update the task as failed or incomplete in the database or internal state
        update_task_status(client_id, "failed", "Disconnected before completion")
    except Exception as e:
        # Handle other exceptions
        print(f"An error occurred: {str(e)}")
        await websocket.close(code=1011)  # Internal error


def update_task_status(client_id, status, message):
    # Assuming we have a session and TaskModel defined as before
    print(f"Update from client {client_id}: status: {status}, message: {message}")
    # with SessionLocal() as session:
    #     task = session.query(TaskModel).filter(TaskModel.client_id == client_id).first()
    #     if task:
    #         task.status = status
    #         task.description = message  # Updating the description or you can add a separate field for messages
    #         session.commit()
    #     else:
    #         print(f"No task found for Client {client_id}")
