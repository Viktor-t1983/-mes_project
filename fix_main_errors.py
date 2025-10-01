import os

# Создаем чистую исправленную версию main.py
fixed_main = '''from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import qrcode
import io
import base64
from typing import List
import traceback

# Импорты моделей и схем
from src.models.order import Order
from src.models.employee import Employee
from src.models.manufacturing_order import ManufacturingOrder
from src.models.operation import Operation
from src.models.defect_report import DefectReport
from src.models.project import Project

from src.schemas.order import Order as OrderSchema
from src.schemas.employee import Employee as EmployeeSchema
from src.schemas.manufacturing_order import ManufacturingOrder as ManufacturingOrderSchema
from src.schemas.operation import Operation as OperationSchema
from src.schemas.defect_report import DefectReport as DefectReportSchema
from src.schemas.project import Project as ProjectSchema

# Используем синхронную БД для стабильности
from create_sync_database import get_db, SessionLocal

app = FastAPI(title="MES System API", version="1.0.0")

@app.get("/")
async def root():
    return {"message": "MES System API", "status": "работает"}

@app.get("/api/v1/health")
async def health_check():
    return {
        "status": "healthy", 
        "database": "postgresql", 
        "timestamp": "2024-01-01T00:00:00Z"
    }

@app.get("/api/v1/orders", response_model=List[OrderSchema])
async def get_orders(db: SessionLocal = Depends(get_db)):
    """Получение всех заказов"""
    try:
        result = db.execute(select(Order))
        orders = result.scalars().all()
        return orders
    except Exception as e:
        print(f"Database error in get_orders: {e}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.get("/api/v1/mo", response_model=List[ManufacturingOrderSchema])
async def get_manufacturing_orders(db: SessionLocal = Depends(get_db)):
    """Получение всех производственных заданий"""
    try:
        result = db.execute(select(ManufacturingOrder))
        mo_list = result.scalars().all()
        return mo_list
    except Exception as e:
        print(f"Database error in get_manufacturing_orders: {e}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.get("/api/v1/employees", response_model=List[EmployeeSchema])
async def get_employees(db: SessionLocal = Depends(get_db)):
    """Получение всех сотрудников"""
    try:
        result = db.execute(select(Employee))
        employees = result.scalars().all()
        return employees
    except Exception as e:
        print(f"Database error in get_employees: {e}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.get("/api/v1/operations", response_model=List[OperationSchema])
async def get_operations(db: SessionLocal = Depends(get_db)):
    """Получение всех операций"""
    try:
        result = db.execute(select(Operation))
        operations = result.scalars().all()
        return operations
    except Exception as e:
        print(f"Database error in get_operations: {e}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.get("/api/v1/defects", response_model=List[DefectReportSchema])
async def get_defects(db: SessionLocal = Depends(get_db)):
    """Получение всех отклонений"""
    try:
        result = db.execute(select(DefectReport))
        defects = result.scalars().all()
        return defects
    except Exception as e:
        print(f"Database error in get_defects: {e}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.get("/api/v1/projects", response_model=List[ProjectSchema])
async def get_projects(db: SessionLocal = Depends(get_db)):
    """Получение всех проектов"""
    try:
        result = db.execute(select(Project))
        projects = result.scalars().all()
        return projects
    except Exception as e:
        print(f"Database error in get_projects: {e}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

# QR код эндпоинты
@app.get("/api/v1/qr/order/{order_id}")
async def generate_order_qr(order_id: int):
    """Генерация QR кода для заказа"""
    try:
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr_data = f"ORDER:{order_id}"
        qr.add_data(qr_data)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)
        
        img_str = base64.b64encode(buffer.getvalue()).decode()
        return {
            "qr_code": f"data:image/png;base64,{img_str}",
            "order_id": order_id,
            "data": qr_data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка генерации QR: {str(e)}")

@app.get("/api/v1/qr/employee/{employee_id}")
async def generate_employee_qr(employee_id: int):
    """Генерация QR кода для сотрудника"""
    try:
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr_data = f"EMPLOYEE:{employee_id}"
        qr.add_data(qr_data)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)
        
        img_str = base64.b64encode(buffer.getvalue()).decode()
        return {
            "qr_code": f"data:image/png;base64,{img_str}",
            "employee_id": employee_id,
            "data": qr_data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка генерации QR: {str(e)}")

@app.get("/api/v1/qr/mo/{mo_id}")
async def generate_mo_qr(mo_id: int):
    """Генерация QR кода для производственного задания"""
    try:
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr_data = f"MO:{mo_id}"
        qr.add_data(qr_data)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)
        
        img_str = base64.b64encode(buffer.getvalue()).decode()
        return {
            "qr_code": f"data:image/png;base64,{img_str}",
            "mo_id": mo_id,
            "data": qr_data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка генерации QR: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
'''

with open('main.py', 'w', encoding='utf-8') as f:
    f.write(fixed_main)

print("✅ Main.py исправлен и готов к работе")
print("🔧 Используется синхронная БД для стабильности")
