from datetime import datetime
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.core.database import engine, get_db
from src.models.base import Base

# Импорт всех моделей для создания таблиц





app = FastAPI(
    title="MES-X v4.0",
    description="Система управления производством для несерийного производства",
    version="0.1.0"
)

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# ========== MANUFACTURING ORDERS ==========
@app.post("/api/v1/mo")
async def create_manufacturing_order(
    order_number: str,
    product_name: str,
    product_code: str,
    quantity: int,
    db: AsyncSession = Depends(get_db)
):
    mo = ManufacturingOrder(
        order_number=order_number,
        product_name=product_name,
        product_code=product_code,
        quantity=quantity,
        status="created"
    )
    db.add(mo)
    await db.commit()
    await db.refresh(mo)
    return {"message": "Производственное задание создано", "id": mo.id}

@app.get("/api/v1/mo")
async def get_manufacturing_orders(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ManufacturingOrder))
    orders = result.scalars().all()
    return orders

# ========== OPERATIONS ==========
@app.post("/api/v1/operations")
async def create_operation(
    manufacturing_order_id: int,
    operation_number: str,
    name: str,
    description: str = "",
    db: AsyncSession = Depends(get_db)
):
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
    result = await db.execute(select(Operation))
    operations = result.scalars().all()
    return operations

@app.post("/api/v1/operations/start")
async def start_operation(
    operation_id: int,
    employee_id: int,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Operation).where(Operation.id == operation_id))
    operation = result.scalar_one_or_none()
    
    if not operation:
        raise HTTPException(status_code=404, detail="Операция не найдена")
    
    operation.status = "in_progress"
    operation.assigned_employee_id = employee_id
    await db.commit()
    
    return {"message": f"Операция {operation_id} запущена сотрудником {employee_id}", "status": "started"}

# ========== ORDERS ==========
@app.post("/api/v1/orders")
async def create_order(
    product_name: str,
    quantity: int,
    db: AsyncSession = Depends(get_db)
):
    order = Order(
        product_name=product_name,
        quantity=quantity,
        status="created"
    )
    db.add(order)
    await db.commit()
    await db.refresh(order)
    return {"message": "Заказ создан", "id": order.id}

@app.get("/api/v1/orders")
async def get_orders(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Order))
    orders = result.scalars().all()
    return orders

# ========== PROJECTS ==========
@app.post("/api/v1/projects")
async def create_project(
    name: str,
    description: str = "",
    db: AsyncSession = Depends(get_db)
):
    project = Project(
        name=name,
        description=description
    )
    db.add(project)
    await db.commit()
    await db.refresh(project)
    return {"message": "Проект создан", "id": project.id}

@app.get("/api/v1/projects")
async def get_projects(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Project))
    projects = result.scalars().all()
    return projects

# ========== EMPLOYEES ==========
@app.post("/api/v1/employees")
async def create_employee(
    first_name: str,
    last_name: str,
    role: str,
    db: AsyncSession = Depends(get_db)
):
    # Генерируем QR код на основе имени и фамилии
    qr_code = f"EMP{first_name[0]}{last_name}".upper()
    
    employee = Employee(
        first_name=first_name,
        last_name=last_name,
        role=role,
        qr_code=qr_code,
        is_active=True
    )
    db.add(employee)
    await db.commit()
    await db.refresh(employee)
    return {"message": "Сотрудник создан", "id": employee.id}

@app.get("/api/v1/employees")
async def get_employees(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Employee))
    employees = result.scalars().all()
    return employees

# ========== QR CODES ==========


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
    """
    Создание отчета о дефекте
    """
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
    result = await db.execute(select(DefectReport))
    defects = result.scalars().all()
    return defects

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

# ========== OPERATION MANAGEMENT ==========
@app.post("/api/v1/operations/pause")
async def pause_operation(
    operation_id: int,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Operation).where(Operation.id == operation_id))
    operation = result.scalar_one_or_none()
    
    if not operation:
        raise HTTPException(status_code=404, detail="Операция не найдена")
    
    operation.status = "paused"
    await db.commit()
    
    return {"message": f"Операция {operation_id} приостановлена", "status": "paused"}

@app.post("/api/v1/operations/complete")
async def complete_operation(
    operation_id: int,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Operation).where(Operation.id == operation_id))
    operation = result.scalar_one_or_none()
    
    if not operation:
        raise HTTPException(status_code=404, detail="Операция не найдена")
    
    operation.status = "completed"
    operation.completed_at = datetime.utcnow()
    await db.commit()
    
    return {"message": f"Операция {operation_id} завершена", "status": "completed"}


        "qr_data": qr_data
        "entity": entity,
        "entity_id": id,
        "qr_data": qr_data,
        "qr_image_url": f"/api/v1/qr/image/{qr_data}"
    }


 {id}",
        "entity": entity, 
        "entity_id": id,
        "qr_data": qr_data
    }


# ========== QR CODE GENERATION ==========
@app.get("/api/v1/qr/{entity}/{id}")
async def generate_qr_code(entity: str, id: int):
    """Генерация QR-кода для сущности"""
    valid_entities = ['order', 'employee', 'mo']
    if entity not in valid_entities:
        raise HTTPException(status_code=400, detail="Неподдерживаемая сущность")
    
    qr_data = f"{entity}_{id}_clean_{hash(f'{entity}{id}') % 10000:04d}"
    
    return {
        "message": f"QR-код для {entity} {id}",
        "entity": entity,
        "entity_id": id,
        "qr_data": qr_data
    }

