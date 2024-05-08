from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str
    admin_email: str
    debug: bool = False  # Default value if not specified

    class Config:
        env_file = '.env'

# Access settings
settings = Settings()

print(f"App Name: {settings.app_name}")
print(f"Admin Email: {settings.admin_email}")
print(f"Debug Mode: {settings.debug}")
