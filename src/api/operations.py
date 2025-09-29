from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from src.core.database import get_db
from src.schemas.operation import Operation, OperationCreate, OperationUpdate
from src.crud.operation import (
    get_operation, get_operations_by_order, get_operations_by_employee,
    create_operation, update_operation, start_operation, complete_operation
)

router = APIRouter(prefix="/operations", tags=["operations"])

@router.get("/", response_model=List[Operation])
def read_operations(
    skip: int = 0,
    limit: int = 100,
    order_id: int = None,
    employee_id: int = None,
    db: Session = Depends(get_db)
):
    if order_id:
        operations = get_operations_by_order(db, manufacturing_order_id=order_id, skip=skip, limit=limit)
    elif employee_id:
        operations = get_operations_by_employee(db, employee_id=employee_id, skip=skip, limit=limit)
    else:
        operations = get_operations_by_order(db, manufacturing_order_id=0, skip=skip, limit=limit)  # Empty result
    return operations

@router.get("/{operation_id}", response_model=Operation)
def read_operation(operation_id: int, db: Session = Depends(get_db)):
    db_operation = get_operation(db, operation_id=operation_id)
    if db_operation is None:
        raise HTTPException(status_code=404, detail="Operation not found")
    return db_operation

@router.post("/", response_model=Operation, status_code=status.HTTP_201_CREATED)
def create_new_operation(operation: OperationCreate, db: Session = Depends(get_db)):
    return create_operation(db=db, operation=operation)

@router.put("/{operation_id}", response_model=Operation)
def update_existing_operation(operation_id: int, operation: OperationUpdate, db: Session = Depends(get_db)):
    db_operation = update_operation(db, operation_id=operation_id, operation=operation)
    if db_operation is None:
        raise HTTPException(status_code=404, detail="Operation not found")
    return db_operation

@router.post("/{operation_id}/start", response_model=Operation)
def start_operation_endpoint(operation_id: int, db: Session = Depends(get_db)):
    db_operation = start_operation(db, operation_id=operation_id)
    if db_operation is None:
        raise HTTPException(status_code=404, detail="Operation not found or cannot be started")
    return db_operation

@router.post("/{operation_id}/complete", response_model=Operation)
def complete_operation_endpoint(
    operation_id: int, 
    quality_check_passed: bool = True,
    db: Session = Depends(get_db)
):
    db_operation = complete_operation(db, operation_id=operation_id, quality_check_passed=quality_check_passed)
    if db_operation is None:
        raise HTTPException(status_code=404, detail="Operation not found or cannot be completed")
    return db_operation
