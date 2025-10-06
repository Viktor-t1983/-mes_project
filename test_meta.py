import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from src.core.config import settings
from src.models.meta_process import MetaProcess

async def test_db():
    engine = create_async_engine(settings.DATABASE_URL)
    async with AsyncSession(engine) as session:
        proc = MetaProcess(name="Test from script")
        session.add(proc)
        await session.commit()
        await session.refresh(proc)  # ← Добавлено
        print(f"✅ Успешно создан процесс ID={proc.id}")

asyncio.run(test_db())
