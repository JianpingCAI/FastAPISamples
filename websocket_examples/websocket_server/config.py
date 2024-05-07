from pydantic import BaseModel


class Settings(BaseModel):
    app_name: str = "WebSocket Task Manager"
    # admin_email: str
    # items_per_user: int = 10

    class Config:
        env_file = ".env"


settings = Settings()
