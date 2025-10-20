from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "")

    def __init__(self, **data):
        super().__init__(**data)
        if not self.DATABASE_URL:
            raise ValueError("DATABASE_URL must be set in .env")
        if not self.SECRET_KEY:
            raise ValueError("SECRET_KEY must be set in .env")

settings = Settings()
