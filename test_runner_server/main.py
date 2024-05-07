from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.responses import JSONResponse
from typing import Dict, List
from router import api_router
from websocket_manager import websocket_endpoint

app = FastAPI()


# Include API routes
app.include_router(api_router)

# WebSocket route
app.websocket("/ws/{runner_id}")(websocket_endpoint)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
