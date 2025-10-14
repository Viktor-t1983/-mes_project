from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:MesProject2025@localhost:5432/mes_db")
    ONE_C_BASE_URL: str = os.getenv("ONE_C_BASE_URL", "")
    ONE_C_USERNAME: str = os.getenv("ONE_C_USERNAME", "")
    ONE_C_PASSWORD: str = os.getenv("ONE_C_PASSWORD", "")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"

settings = Settings()
