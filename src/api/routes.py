from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update
import json
from datetime import datetime
from typing import List

from src.core.database import get_db
from src.models.employee import Employee as EmployeeModel
from src.models.manufacturing_order import ManufacturingOrder as MOModel
from src.models.operation import Operation as OperationModel
from src.models.defect_report import DefectReport as DefectModel

from src.schemas.manufacturing_order import ManufacturingOrderCreate, ManufacturingOrder
from src.schemas.operation import OperationStart, OperationPause, OperationComplete
from src.schemas.defect_report import DefectReportCreate, DefectReport

from src.utils.qrcode_generator import generate_qr_code

router = APIRouter()
# ==================== ДЕНЬ 3: ЯДРО ПРОИЗВОДСТВА ====================

# --- Manufacturing Orders ---
@router.post("/mo", response_model=ManufacturingOrder)
async def create_mo(mo: ManufacturingOrderCreate, db: AsyncSession = Depends(get_db)):
    db_mo = MOModel(**mo.model_dump())
    db.add(db_mo)
    await db.commit()
    await db.refresh(db_mo)
    return db_mo

@router.get("/mo", response_model=List[ManufacturingOrder])
async def get_mos(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(MOModel).offset(skip).limit(limit))
    return result.scalars().all()

# --- Operations ---
@router.post("/operations/start")
async def start_operation(data: OperationStart, db: AsyncSession = Depends(get_db)):
    # Проверка сотрудника
    emp = await db.scalar(select(EmployeeModel).where(EmployeeModel.qr_code == data.employee_qr))
    if not emp or not emp.is_active:
        raise HTTPException(403, "Сотрудник не найден или неактивен")
    
    # Проверка допуска к станку
    allowed_centers = json.loads(emp.allowed_workcenters) if emp.allowed_workcenters else []
    if data.workcenter_id not in allowed_centers:
        raise HTTPException(403, "Нет допуска к станку")

    # Создаём операцию
    op = OperationModel(
        mo_id=data.mo_id,
        employee_id=emp.id,
        workcenter_id=data.workcenter_id,
        operation_type="custom",
        status="in_progress",
        start_time=datetime.utcnow(),
        qr_code=f"MO-{data.mo_id}-OP-{emp.id}"
    )
    db.add(op)
    await db.commit()
    await db.refresh(op)
    
    # Обновляем статус MO
    await db.execute(update(MOModel).where(
        MOModel.id == data.mo_id
    ).values(status="in_progress", current_operation_id=op.id))
    await db.commit()
    
    return {"operation_id": op.id, "qr_code": op.qr_code, "status": "started"}

@router.post("/operations/pause")
async def pause_operation(data: OperationPause, db: AsyncSession = Depends(get_db)):
    op = await db.get(OperationModel, data.operation_id)
    if not op or op.status != "in_progress":
        raise HTTPException(400, "Операция не в работе")
    
    pauses = json.loads(op.pause_events) if op.pause_events else []
    pauses.append({"start": datetime.utcnow().isoformat(), "reason": data.reason})
    op.pause_events = json.dumps(pauses)
    op.status = "paused"
    await db.commit()
    return {"status": "paused", "operation_id": op.id}

@router.post("/operations/complete")
async def complete_operation(data: OperationComplete, db: AsyncSession = Depends(get_db)):
    emp = await db.scalar(select(EmployeeModel).where(EmployeeModel.qr_code == data.employee_qr))
    if not emp:
        raise HTTPException(403, "Подтверждение: сотрудник не найден")
    
    op = await db.get(OperationModel, data.operation_id)
    if not op:
        raise HTTPException(404, "Операция не найдена")
    
    op.end_time = datetime.utcnow()
    op.status = "completed"
    await db.commit()
    
    # Обновляем статус MO если все операции завершены
    await db.execute(update(MOModel).where(
        MOModel.id == op.mo_id
    ).values(status="completed", current_operation_id=None))
    await db.commit()
    
    return {"status": "completed", "operation_id": op.id}

# --- QR-коды ---
@router.get("/qr/{entity_type}/{entity_id}")
async def get_qr(entity_type: str, entity_id: int, db: AsyncSession = Depends(get_db)):
    if entity_type == "mo":
        mo = await db.get(MOModel, entity_id)
        if not mo:
            raise HTTPException(404, "MO не найден")
        qr_data = f"MO-{mo.id}"
    elif entity_type == "order":
        order = await db.get(OrderModel, entity_id)
        if not order:
            raise HTTPException(404, "Заказ не найден")
        qr_data = f"ORDER-{order.id}"
    elif entity_type == "employee":
        employee = await db.scalar(select(EmployeeModel).where(EmployeeModel.id == entity_id))
        if not employee:
            raise HTTPException(404, "Сотрудник не найден")
        qr_data = employee.qr_code
    else:
        raise HTTPException(400, "Неподдерживаемый тип")
    
    qr_image = generate_qr_code(qr_data)
    return Response(content=qr_image, media_type="image/png")

# --- Отклонения ---
@router.post("/defects", response_model=DefectReport)
async def create_defect(defect: DefectReportCreate, db: AsyncSession = Depends(get_db)):
    db_defect = DefectModel(**defect.model_dump())
    db.add(db_defect)
    await db.commit()
    await db.refresh(db_defect)
    
    # Если срочно — ставим связанные задания на паузу
    if defect.is_urgent:
        if defect.entity_type == "mo":
            await db.execute(update(MOModel).where(
                MOModel.id == defect.entity_id
            ).values(status="on_hold"))
        elif defect.entity_type == "operation":
            await db.execute(update(OperationModel).where(
                OperationModel.id == defect.entity_id
            ).values(status="on_hold"))
        await db.commit()
    
    return db_defect

@router.get("/defects", response_model=List[DefectReport])
async def get_defects(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(DefectModel).offset(skip).limit(limit))
    return result.scalars().all()

# Health check
@router.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow()}