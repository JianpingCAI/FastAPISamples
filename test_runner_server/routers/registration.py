from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from uuid import uuid4
from models import runners_details, Runner

router = APIRouter()

class RegistrationData(BaseModel):
    capabilities: dict
    status: str

@router.post("/{runner_id}")
async def register_runner(runner_id: int, data: RegistrationData):
    if runner_id in runners_details:
        raise HTTPException(status_code=400, detail="Runner already registered")
    new_runner = Runner(runner_id=runner_id, capabilities=data.capabilities, status=data.status)
    runners_details[runner_id] = new_runner
    return {"runner_id": runner_id, "message": "Runner registered successfully"}
