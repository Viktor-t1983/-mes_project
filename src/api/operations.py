from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from src import schemas, models
from src.core.database import get_db
from src.core.dependencies import get_current_employee
from src.schemas.operation import Operation, OperationCreate, OperationUpdate, OperationPause
from src.crud.operation import (
    get_operation, get_operations_by_order, get_operations_by_employee,
    create_operation, update_operation, start_operation, complete_operation,
    pause_operation, resume_operation
)
import src.crud as crud

router = APIRouter(prefix="/operations", tags=["operations"])

@router.get("/", response_model=List[Operation])
def read_operations(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    operations = crud.operation.get_operations_by_order(db, skip=skip, limit=limit)
    return operations

@router.get("/{operation_id}", response_model=Operation)
def read_operation(operation_id: int, db: Session = Depends(get_db)):
    db_operation = crud.operation.get_operation(db, operation_id=operation_id)
    if db_operation is None:
        raise HTTPException(status_code=404, detail="Operation not found")
    return db_operation

@router.post("/", response_model=Operation)
def create_operation_endpoint(
    operation: OperationCreate,
    db: Session = Depends(get_db)
):
    return crud.operation.create_operation(db=db, operation=operation)

@router.put("/{operation_id}", response_model=Operation)
def update_operation_endpoint(
    operation_id: int,
    operation: OperationUpdate,
    db: Session = Depends(get_db)
):
    db_operation = crud.operation.update_operation(db, operation_id=operation_id, operation=operation)
    if db_operation is None:
        raise HTTPException(status_code=404, detail="Operation not found")
    return db_operation

@router.post("/{operation_id}/start", response_model=Operation)
def start_operation_endpoint(operation_id: int, db: Session = Depends(get_db)):
    db_operation = crud.operation.start_operation(db, operation_id=operation_id)
    if db_operation is None:
        raise HTTPException(status_code=404, detail="Operation not found or cannot be started")
    return db_operation

@router.post("/{operation_id}/complete", response_model=Operation)
def complete_operation_endpoint(
    operation_id: int,
    quality_check_passed: bool = True,
    db: Session = Depends(get_db)
):
    db_operation = crud.operation.complete_operation(db, operation_id=operation_id, quality_check_passed=quality_check_passed)
    if db_operation is None:
        raise HTTPException(status_code=404, detail="Operation not found or cannot be completed")
    return db_operation

@router.post("/{operation_id}/pause", response_model=schemas.Operation)
def pause_operation_endpoint(
    operation_id: int,
    pause_data: OperationPause,
    db: Session = Depends(get_db),
    current_employee: models.Employee = Depends(get_current_employee)
):
    """
    Поставить операцию на паузу.
    Требуются права оператора или выше.
    """
    db_operation = crud.operation.get_operation(db, operation_id=operation_id)
    if not db_operation:
        raise HTTPException(status_code=404, detail="Operation not found")
    
    # Проверяем что операция в статусе 'in_progress'
    if db_operation.status != "in_progress":
        raise HTTPException(
            status_code=400, 
            detail="Можно ставить на паузу только операции в процессе выполнения"
        )
    
    # Проверяем права сотрудника
    if current_employee.role not in ["operator", "master", "inspector"]:
        raise HTTPException(
            status_code=403,
            detail="Недостаточно прав для выполнения этой операции"
        )
    
    # Ставим операцию на паузу
    updated_operation = crud.operation.pause_operation(
        db, 
        operation_id=operation_id,
        reason=pause_data.reason
    )
    
    return updated_operation

@router.post("/{operation_id}/resume", response_model=schemas.Operation)
def resume_operation_endpoint(
    operation_id: int,
    db: Session = Depends(get_db),
    current_employee: models.Employee = Depends(get_current_employee)
):
    """
    Возобновить операцию после паузы.
    Требуются права оператора или выше.
    """
    db_operation = crud.operation.get_operation(db, operation_id=operation_id)
    if not db_operation:
        raise HTTPException(status_code=404, detail="Operation not found")
    
    # Проверяем что операция в статусе 'paused'
    if db_operation.status != "paused":
        raise HTTPException(
            status_code=400, 
            detail="Можно возобновлять только операции на паузе"
        )
    
    # Проверяем права сотрудника
    if current_employee.role not in ["operator", "master", "inspector"]:
        raise HTTPException(
            status_code=403,
            detail="Недостаточно прав для выполнения этой операции"
        )
    
    # Возобновляем операцию
    updated_operation = crud.operation.resume_operation(db, operation_id=operation_id)
    
    return updated_operation
