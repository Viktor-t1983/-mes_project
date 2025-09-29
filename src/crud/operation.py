from sqlalchemy.orm import Session
from sqlalchemy import and_
from src.models.operation import Operation
from src.schemas.operation import OperationCreate, OperationUpdate

def get_operation(db: Session, operation_id: int):
    return db.query(Operation).filter(Operation.id == operation_id).first()

def get_operations_by_order(db: Session, manufacturing_order_id: int, skip: int = 0, limit: int = 100):
    return db.query(Operation).filter(
        Operation.manufacturing_order_id == manufacturing_order_id
    ).offset(skip).limit(limit).all()

def get_operations_by_employee(db: Session, employee_id: int, skip: int = 0, limit: int = 100):
    return db.query(Operation).filter(
        Operation.assigned_employee_id == employee_id
    ).offset(skip).limit(limit).all()

def create_operation(db: Session, operation: OperationCreate):
    db_operation = Operation(
        manufacturing_order_id=operation.manufacturing_order_id,
        operation_number=operation.operation_number,
        name=operation.name,
        description=operation.description,
        planned_duration=operation.planned_duration,
        assigned_employee_id=operation.assigned_employee_id,
        status=operation.status,
        notes=operation.notes
    )
    db.add(db_operation)
    db.commit()
    db.refresh(db_operation)
    return db_operation

def update_operation(db: Session, operation_id: int, operation: OperationUpdate):
    db_operation = db.query(Operation).filter(Operation.id == operation_id).first()
    if db_operation:
        update_data = operation.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_operation, field, value)
        db.commit()
        db.refresh(db_operation)
    return db_operation

def start_operation(db: Session, operation_id: int):
    db_operation = db.query(Operation).filter(Operation.id == operation_id).first()
    if db_operation and db_operation.status == "pending":
        db_operation.status = "in_progress"
        from datetime import datetime
        db_operation.started_at = datetime.now()
        db.commit()
        db.refresh(db_operation)
    return db_operation

def complete_operation(db: Session, operation_id: int, quality_check_passed: bool = True):
    db_operation = db.query(Operation).filter(Operation.id == operation_id).first()
    if db_operation and db_operation.status == "in_progress":
        db_operation.status = "completed"
        db_operation.quality_check_passed = quality_check_passed
        from datetime import datetime
        db_operation.completed_at = datetime.now()
        db.commit()
        db.refresh(db_operation)
    return db_operation
