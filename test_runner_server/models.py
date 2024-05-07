from fastapi import WebSocket
from typing import Dict, Optional


class Runner:
    def __init__(self, runner_id: int, capabilities: dict, status: str):
        self.runner_id = runner_id
        self.capabilities = capabilities
        self.status = status


# Dictionary to hold active WebSocket connections
active_connections: Dict[int, WebSocket] = {}

# Optional: Dictionary to hold runner metadata if needed for other operations
runners_details: Dict[int, Runner] = {}
