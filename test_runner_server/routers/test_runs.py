from typing import List
from fastapi import APIRouter, Depends, HTTPException, WebSocket
from pydantic import BaseModel
from yaml import dump
from test_runner_server.models import runners  # Import the shared state

router = APIRouter()


class TestRun(BaseModel):
    description: str
    test_cases: List[dict]


@router.post("/execute/{runner_id}/")
async def send_test_run(runner_id: int, test_run: TestRun):
    if runner_id not in runners:
        raise HTTPException(status_code=404, detail="Runner not found")
    yaml_data = dump(test_run.dict())
    websocket:WebSocket = runners[runner_id]
    await websocket.send_text(yaml_data)  # Send YAML data to the runner
    return {"message": "Test run sent to runner"}
