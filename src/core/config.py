import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # Явно указываем psycopg2 драйвер
    DATABASE_URL = "postgresql://postgres:MesProject2025@localhost:5432/mes_db"
    
settings = Settings()
