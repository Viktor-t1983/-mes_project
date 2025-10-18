import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-fallback-key")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    ONE_C_BASE_URL: str = os.getenv("ONE_C_BASE_URL", "")
    ONE_C_USER: str = os.getenv("ONE_C_USER", "")
    ONE_C_PASSWORD: str = os.getenv("ONE_C_PASSWORD", "")

    def __init__(self, **data):
        super().__init__(**data)
        if not self.DATABASE_URL:
            raise ValueError("DATABASE_URL must be set in .env")

settings = Settings()
