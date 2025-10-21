from fastapi import FastAPI
from src.core.database import engine
from src.models import Base

# Импортируем все роутеры
from src.api import (
    qr_codes_router,
    employees_router,
    manufacturing_orders_router,
    operations_router,
    defect_reports_router,
    warehouse_items_router,
    incentives_router
)

# Создаем таблицы (если их нет)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="MES System API",
    description="Manufacturing Execution System API - Complete MES solution",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Подключаем все роутеры
app.include_router(employees_router, prefix="/api/v1", tags=["employees"])
app.include_router(manufacturing_orders_router, prefix="/api/v1", tags=["manufacturing-orders"])
app.include_router(operations_router, prefix="/api/v1", tags=["operations"])
app.include_router(defect_reports_router, prefix="/api/v1", tags=["defect-reports"])
app.include_router(warehouse_items_router, prefix="/api/v1", tags=["warehouse-items"])
app.include_router(incentives_router, prefix="/api/v1", tags=["incentives"])
app.include_router(qr_codes_router, prefix="/api/v1", tags=["qr-codes"])

@app.get("/")
def read_root():
    return {
        "message": "MES System API is running!",
        "version": "2.0.0",
        "docs": "/docs",
        "modules": [
            "employees", 
            "manufacturing-orders", 
            "operations", 
            "defect-reports", 
            "warehouse-items", 
            "incentives"
        ]
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy", 
        "database": "connected",
        "modules": 6
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)