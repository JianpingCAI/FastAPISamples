# registration.py
import requests
from config import SERVER_URL, RUNNER_CAPABILITIES


def register_with_server():
    response = requests.post(f"{SERVER_URL}/register", json=RUNNER_CAPABILITIES)
    if response.status_code == 200:
        return response.json()["runner_id"]
    else:
        raise Exception("Failed to register with the server")
