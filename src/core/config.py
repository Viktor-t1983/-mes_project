import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DATABASE_URL = "postgresql+asyncpg://postgres:MesProject2025@localhost:5432/mes_db"

settings = Settings()
