from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.core.database import get_db
from src.models.project import Project as ProjectModel
from src.schemas.project import ProjectCreate, ProjectUpdate, Project
from src.services.operation_service import (
    create_operation, get_operation, update_operation,
    start_operation, complete_operation, report_defect,
    get_operation_by_qr
)
from src.services.employee_service import create_employee, get_employee, get_employee_by_qr
from src.schemas.operation import OperationCreate, OperationUpdate, Operation
from src.schemas.employee import EmployeeCreate, EmployeeUpdate, Employee

router = APIRouter()

# === Project Routes ===
@router.get("/projects", response_model=list[Project])
async def get_projects(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ProjectModel))
    projects = result.scalars().all()
    return projects

@router.post("/projects", response_model=Project)
async def create_project(project: ProjectCreate, db: AsyncSession = Depends(get_db)):
    db_project = ProjectModel(**project.model_dump())
    db.add(db_project)
    await db.commit()
    await db.refresh(db_project)
    return db_project

@router.get("/projects/{project_id}", response_model=Project)
async def get_project(project_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ProjectModel).where(ProjectModel.id == project_id))
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

# === Employee Routes ===
@router.post("/employees", response_model=Employee)
async def create_employee_endpoint(employee: EmployeeCreate, db: AsyncSession = Depends(get_db)):
    return await create_employee(db, employee)

@router.get("/employees/{employee_id}", response_model=Employee)
async def get_employee_endpoint(employee_id: int, db: AsyncSession = Depends(get_db)):
    employee = await get_employee(db, employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee

@router.get("/employees/qr/{qr_code}", response_model=Employee)
async def get_employee_by_qr_endpoint(qr_code: str, db: AsyncSession = Depends(get_db)):
    employee = await get_employee_by_qr(db, qr_code)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee

# === Operation Routes ===
@router.post("/operations", response_model=Operation)
async def create_operation_endpoint(operation: OperationCreate, db: AsyncSession = Depends(get_db)):
    return await create_operation(db, operation)

@router.get("/operations/{operation_id}", response_model=Operation)
async def get_operation_endpoint(operation_id: int, db: AsyncSession = Depends(get_db)):
    operation = await get_operation(db, operation_id)
    if not operation:
        raise HTTPException(status_code=404, detail="Operation not found")
    return operation

@router.get("/operations/qr/{qr_code}", response_model=Operation)
async def get_operation_by_qr_endpoint(qr_code: str, db: AsyncSession = Depends(get_db)):
    operation = await get_operation_by_qr(db, qr_code)
    if not operation:
        raise HTTPException(status_code=404, detail="Operation not found")
    return operation

@router.put("/operations/{operation_id}", response_model=Operation)
async def update_operation_endpoint(operation_id: int, operation: OperationUpdate, db: AsyncSession = Depends(get_db)):
    updated_op = await update_operation(db, operation_id, operation)
    if not updated_op:
        raise HTTPException(status_code=404, detail="Operation not found")
    return updated_op

# === Production Execution Routes ===
@router.post("/operations/{operation_id}/start")
async def start_operation_endpoint(operation_id: int, employee_id: int, db: AsyncSession = Depends(get_db)):
    operation = await start_operation(db, operation_id, employee_id)
    if not operation:
        raise HTTPException(status_code=404, detail="Operation not found or already started")
    return {"message": "Operation started successfully", "operation_id": operation.id}

@router.post("/operations/{operation_id}/complete")
async def complete_operation_endpoint(operation_id: int, db: AsyncSession = Depends(get_db)):
    operation = await complete_operation(db, operation_id)
    if not operation:
        raise HTTPException(status_code=404, detail="Operation not found or not in progress")
    return {"message": "Operation completed successfully", "operation_id": operation.id}

@router.post("/operations/{operation_id}/defect")
async def report_defect_endpoint(operation_id: int, reason: str, db: AsyncSession = Depends(get_db)):
    operation = await report_defect(db, operation_id, reason)
    if not operation:
        raise HTTPException(status_code=404, detail="Operation not found")
    return {"message": "Defect reported successfully", "operation_id": operation.id}

# === QR Scan Simulation ===
@router.post("/scan")
async def scan_qr(
    operation_qr: str = Query(..., description="QR-код операции"),
    employee_qr: str = Query(..., description="QR-код сотрудника"), 
    action: str = Query(..., description="Действие: start, complete, defect"),
    db: AsyncSession = Depends(get_db)
):
    """
    Эмуляция сканирования QR-кодов с мобильного устройства
    Actions: start, complete, defect
    """
    # Проверяем сотрудника
    employee = await get_employee_by_qr(db, employee_qr)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    # Проверяем операцию
    operation = await get_operation_by_qr(db, operation_qr)
    if not operation:
        raise HTTPException(status_code=404, detail="Operation not found")

    # Выполняем действие
    if action == "start":
        result = await start_operation(db, operation.id, employee.id)
        message = "Operation started"
    elif action == "complete":
        result = await complete_operation(db, operation.id)
        message = "Operation completed"
    elif action == "defect":
        result = await report_defect(db, operation.id, "Defect reported via QR scan")
        message = "Defect reported"
    else:
        raise HTTPException(status_code=400, detail="Invalid action")

    if not result:
        raise HTTPException(status_code=400, detail=f"Cannot {action} operation")

    return {
        "message": message,
        "operation": operation.name,
        "employee": employee.name,
        "status": result.status
    }
