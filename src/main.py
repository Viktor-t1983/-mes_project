from fastapi import FastAPI
from src.core.database import engine
from src.models import Base

# Создаем таблицы (если их нет)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="MES System API",
    description="Manufacturing Execution System API",
    version="1.0.0"
)

@app.get("/")
def read_root():
    return {"message": "MES System API is running on port 8001!"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "port": 8001, "database": "connected"}

@app.get("/test")
def test_endpoint():
    return {"test": "success", "data": "API is working with database!"}

# Подключаем роутеры
from src.api.employees import router as employees_router
app.include_router(employees_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
