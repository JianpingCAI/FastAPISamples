from fastapi import APIRouter
from routers.commands import router as commands_router
from  routers.registration import router as registration_router

api_router = APIRouter()
api_router.include_router(commands_router, prefix="/commands", tags=["Commands"])
api_router.include_router(registration_router, prefix="/registration", tags=["Registration"])
