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
