from fastapi import FastAPI
from src.core.database import engine
from src.models.base import Base
from src.api.routes import router

app = FastAPI(
    title="MES-X v4.0",
    description="Система управления производством для несерийного производства",
    version="0.1.0"
)

# Подключаем роутер
app.include_router(router, prefix="/api/v1")

# Создаем таблицы при старте
@app.on_event("startup")
async def startup_event():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/")
def read_root():
    return {"message": "Добро пожаловать в MES-X v4.0!"}

@app.get("/health")
def health_check():
    return {"status": "OK", "version": "0.1.0"}
