import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Синхронный URL (заменяем asyncpg на psycopg2)
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql+asyncpg://postgres:MesProject2025@localhost:5432/mes_db')
SYNC_DATABASE_URL = DATABASE_URL.replace('postgresql+asyncpg://', 'postgresql://')

# Создаем синхронный engine
engine = create_engine(
    SYNC_DATABASE_URL,
    echo=True,
    pool_pre_ping=True,  # Проверка соединения перед использованием
    pool_recycle=3600,   # Переподключение каждый час
)

# Создаем синхронную сессию
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

print("✅ Synchronous database configuration created")
print(f"Database URL: {SYNC_DATABASE_URL}")
