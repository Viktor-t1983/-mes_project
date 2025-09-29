from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.models.operation import Operation
from src.models.employee import Employee
from src.schemas.operation import OperationCreate, OperationUpdate
from datetime import datetime
import random
import string

def generate_qr_code(length=8):
    """Генерация уникального QR-кода"""
    chars = string.ascii_uppercase + string.digits
    return 'OP_' + ''.join(random.choice(chars) for _ in range(length))

async def create_operation(db: AsyncSession, operation: OperationCreate):
    # Генерируем QR-код если не предоставлен
    qr_code = operation.qr_code or generate_qr_code()
    
    db_operation = Operation(
        name=operation.name,
        description=operation.description,
        planned_duration=operation.planned_duration,
        qr_code=qr_code
    )
    db.add(db_operation)
    await db.commit()
    await db.refresh(db_operation)
    return db_operation

async def get_operation(db: AsyncSession, operation_id: int):
    result = await db.execute(select(Operation).where(Operation.id == operation_id))
    return result.scalar_one_or_none()

async def get_operation_by_qr(db: AsyncSession, qr_code: str):
    result = await db.execute(select(Operation).where(Operation.qr_code == qr_code))
    return result.scalar_one_or_none()

async def update_operation(db: AsyncSession, operation_id: int, operation_update: OperationUpdate):
    result = await db.execute(select(Operation).where(Operation.id == operation_id))
    db_operation = result.scalar_one_or_none()
    if db_operation:
        update_data = operation_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_operation, field, value)
        await db.commit()
        await db.refresh(db_operation)
    return db_operation

async def start_operation(db: AsyncSession, operation_id: int, employee_id: int):
    result = await db.execute(select(Operation).where(Operation.id == operation_id))
    db_operation = result.scalar_one_or_none()
    
    if db_operation and db_operation.status == "pending":
        db_operation.status = "in_progress"
        db_operation.employee_id = employee_id
        db_operation.start_time = datetime.utcnow()
        await db.commit()
        await db.refresh(db_operation)
    
    return db_operation

async def complete_operation(db: AsyncSession, operation_id: int):
    result = await db.execute(select(Operation).where(Operation.id == operation_id))
    db_operation = result.scalar_one_or_none()
    
    if db_operation and db_operation.status == "in_progress":
        db_operation.status = "completed"
        db_operation.end_time = datetime.utcnow()
        
        # Расчет фактического времени
        if db_operation.start_time:
            duration = (db_operation.end_time - db_operation.start_time).total_seconds() / 60
            db_operation.actual_duration = int(duration)
        
        await db.commit()
        await db.refresh(db_operation)
    
    return db_operation

async def report_defect(db: AsyncSession, operation_id: int, reason: str):
    result = await db.execute(select(Operation).where(Operation.id == operation_id))
    db_operation = result.scalar_one_or_none()
    
    if db_operation:
        db_operation.status = "defect"
        db_operation.defect_reason = reason
        db_operation.end_time = datetime.utcnow()
        await db.commit()
        await db.refresh(db_operation)
    
    return db_operation
