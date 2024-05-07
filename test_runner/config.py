# config.py
from pydantic import BaseSettings

class Settings(BaseSettings):
    server_url: str = 'http://example.com/api'
    websocket_url: str = 'ws://example.com/test_runner_ws'
    runner_capabilities: dict = {
        "os": "Windows 10",
        "software": ["Python", "ChromeDriver"]
    }

    class Config:
        env_file = ".env"

config = Settings()
