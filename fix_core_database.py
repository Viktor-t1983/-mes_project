"""
Убедимся что core/database.py использует синхронное подключение
"""

database_content = '''from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

# Используем синхронное подключение для SQLAlchemy
DATABASE_URL = os.getenv("DATABASE_URL")

if "asyncpg" in DATABASE_URL:
    # Заменяем asyncpg на psycopg2 для синхронной работы
    DATABASE_URL = DATABASE_URL.replace("asyncpg", "psycopg2")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL not found in environment variables")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

print("✅ Synchronous database configuration created")
print(f"Database URL: {DATABASE_URL}")
'''

with open("src/core/database.py", "w", encoding="utf-8") as f:
    f.write(database_content)

print("✅ src/core/database.py обновлен для синхронной работы")
