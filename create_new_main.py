# Создаем новый корректный main.py
new_content = '''from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select
from datetime import datetime
import os

from src.models.order import Order
from src.models.employee import Employee
from src.models.manufacturing_order import ManufacturingOrder
from src.models.operation import Operation
from src.models.defect_report import DefectReport
from src.models.project import Project

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:password@localhost/mes_system")
engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

app = FastAPI(title="MES-X Production System", version="4.0")

# Dependency
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

# ========== ORDERS ==========
@app.post("/api/v1/orders")
async def create_order(product_name: str, quantity: int, db: AsyncSession = Depends(get_db)):
    """Создание заказа"""
    order = Order(product_name=product_name, quantity=quantity, status="created")
    db.add(order)
    await db.commit()
    await db.refresh(order)
    return {"message": "Заказ создан", "id": order.id}

@app.get("/api/v1/orders")
async def get_orders(db: AsyncSession = Depends(get_db)):
    """Получение всех заказов"""
    result = await db.execute(select(Order))
    orders = result.scalars().all()
    return orders

# ========== MANUFACTURING ORDERS ==========
@app.post("/api/v1/mo")
async def create_manufacturing_order(
    order_number: str,
    product_name: str,
    product_code: str,
    quantity: int,
    priority: str = "normal",
    db: AsyncSession = Depends(get_db)
):
    """Создание производственного задания"""
    mo = ManufacturingOrder(
        order_number=order_number,
        product_name=product_name,
        product_code=product_code,
        quantity=quantity,
        priority=priority,
        status="created"
    )
    db.add(mo)
    await db.commit()
    await db.refresh(mo)
    return {"message": "Производственное задание создано", "id": mo.id}

@app.get("/api/v1/mo")
async def get_manufacturing_orders(db: AsyncSession = Depends(get_db)):
    """Получение всех производственных заданий"""
    result = await db.execute(select(ManufacturingOrder))
    mo_list = result.scalars().all()
    return mo_list

# ========== EMPLOYEES ==========
@app.post("/api/v1/employees")
async def create_employee(
    first_name: str,
    last_name: str,
    role: str,
    db: AsyncSession = Depends(get_db)
):
    """Создание сотрудника"""
    employee = Employee(
        first_name=first_name,
        last_name=last_name,
        role=role,
        is_active=True
    )
    db.add(employee)
    await db.commit()
    await db.refresh(employee)
    return {"message": "Сотрудник создан", "id": employee.id}

@app.get("/api/v1/employees")
async def get_employees(db: AsyncSession = Depends(get_db)):
    """Получение всех сотрудников"""
    result = await db.execute(select(Employee))
    employees = result.scalars().all()
    return employees

# ========== OPERATIONS ==========
@app.post("/api/v1/operations")
async def create_operation(
    manufacturing_order_id: int,
    operation_number: str,
    name: str,
    description: str = None,
    db: AsyncSession = Depends(get_db)
):
    """Создание операции"""
    operation = Operation(
        manufacturing_order_id=manufacturing_order_id,
        operation_number=operation_number,
        name=name,
        description=description,
        status="pending"
    )
    db.add(operation)
    await db.commit()
    await db.refresh(operation)
    return {"message": "Операция создана", "id": operation.id}

@app.get("/api/v1/operations")
async def get_operations(db: AsyncSession = Depends(get_db)):
    """Получение всех операций"""
    result = await db.execute(select(Operation))
    operations = result.scalars().all()
    return operations

@app.post("/api/v1/operations/start")
async def start_operation(operation_id: int, employee_id: int, db: AsyncSession = Depends(get_db)):
    """Запуск операции"""
    result = await db.execute(select(Operation).where(Operation.id == operation_id))
    operation = result.scalar_one_or_none()
    
    if not operation:
        raise HTTPException(status_code=404, detail="Операция не найдена")
    
    operation.status = "in_progress"
    operation.assigned_employee_id = employee_id
    operation.started_at = datetime.utcnow()
    await db.commit()
    
    return {"message": f"Операция {operation_id} запущена сотрудником {employee_id}", "status": "started"}

@app.post("/api/v1/operations/pause")
async def pause_operation(operation_id: int, db: AsyncSession = Depends(get_db)):
    """Приостановка операции"""
    result = await db.execute(select(Operation).where(Operation.id == operation_id))
    operation = result.scalar_one_or_none()
    
    if not operation:
        raise HTTPException(status_code=404, detail="Операция не найдена")
    
    if operation.status != "in_progress":
        raise HTTPException(status_code=400, detail="Можно приостанавливать только выполняющиеся операции")
    
    operation.status = "paused"
    await db.commit()
    
    return {"message": f"Операция {operation_id} приостановлена", "status": "paused"}

@app.post("/api/v1/operations/complete")
async def complete_operation(operation_id: int, db: AsyncSession = Depends(get_db)):
    """Завершение операции"""
    result = await db.execute(select(Operation).where(Operation.id == operation_id))
    operation = result.scalar_one_or_none()
    
    if not operation:
        raise HTTPException(status_code=404, detail="Операция не найдена")
    
    operation.status = "completed"
    operation.completed_at = datetime.utcnow()
    await db.commit()
    
    return {"message": f"Операция {operation_id} завершена", "status": "completed"}

# ========== DEFECTS ==========
@app.post("/api/v1/defects")
async def create_defect_report(
    manufacturing_order_id: int,
    operation_id: int,
    reported_by: int,
    description: str,
    defect_type: str = "качество",
    severity: str = "medium",
    quantity_affected: int = 1,
    db: AsyncSession = Depends(get_db)
):
    """Создание отчета о дефекте"""
    defect = DefectReport(
        manufacturing_order_id=manufacturing_order_id,
        operation_id=operation_id,
        reported_by=reported_by,
        defect_description=description,
        defect_type=defect_type,
        severity=severity,
        quantity_affected=quantity_affected,
        status="reported"
    )
    db.add(defect)
    await db.commit()
    await db.refresh(defect)
    return {"message": "Брак зарегистрирован", "id": defect.id}

@app.get("/api/v1/defects")
async def get_defects(db: AsyncSession = Depends(get_db)):
    """Получение всех дефектов"""
    result = await db.execute(select(DefectReport))
    defects = result.scalars().all()
    return defects

# ========== PROJECTS ==========
@app.post("/api/v1/projects")
async def create_project(name: str, description: str = None, db: AsyncSession = Depends(get_db)):
    """Создание проекта"""
    project = Project(name=name, description=description)
    db.add(project)
    await db.commit()
    await db.refresh(project)
    return {"message": "Проект создан", "id": project.id}

@app.get("/api/v1/projects")
async def get_projects(db: AsyncSession = Depends(get_db)):
    """Получение всех проектов"""
    result = await db.execute(select(Project))
    projects = result.scalars().all()
    return projects

# ========== QR CODE GENERATION ==========
@app.get("/api/v1/qr/{entity}/{id}")
async def generate_qr_code(entity: str, id: int):
    """Генерация QR-кода для сущности"""
    valid_entities = ["order", "employee", "mo"]
    if entity not in valid_entities:
        raise HTTPException(status_code=400, detail="Неподдерживаемая сущность")
    
    qr_data = f"{entity}_{id}_clean_{hash(f'{entity}{id}') % 10000:04d}"
    
    return {
        "message": f"QR-код для {entity} {id}",
        "entity": entity,
        "entity_id": id,
        "qr_data": qr_data
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
'''

with open('main.py', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("✅ Создан новый корректный main.py")
print("📋 Включены все основные эндпоинты:")
print("   - Orders, MO, Employees, Operations, Defects, Projects")
print("   - QR-коды для order, employee, mo")
print("   - Управление операциями (start/pause/complete)")
