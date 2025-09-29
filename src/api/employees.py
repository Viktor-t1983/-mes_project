from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from src.core.database import get_db
from src.schemas.employee import Employee, EmployeeCreate, EmployeeUpdate
from src.crud.employee import (
    get_employee, get_employee_by_qr, get_employees, 
    create_employee, update_employee, delete_employee
)

router = APIRouter(prefix="/employees", tags=["employees"])

@router.get("/", response_model=List[Employee])
def read_employees(
    skip: int = 0, 
    limit: int = 100, 
    active_only: bool = True,
    db: Session = Depends(get_db)
):
    employees = get_employees(db, skip=skip, limit=limit, active_only=active_only)
    return employees

@router.get("/{employee_id}", response_model=Employee)
def read_employee(employee_id: int, db: Session = Depends(get_db)):
    db_employee = get_employee(db, employee_id=employee_id)
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return db_employee

@router.get("/qr/{qr_code}", response_model=Employee)
def read_employee_by_qr(qr_code: str, db: Session = Depends(get_db)):
    db_employee = get_employee_by_qr(db, qr_code=qr_code)
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return db_employee

@router.post("/", response_model=Employee, status_code=status.HTTP_201_CREATED)
def create_new_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):
    db_employee = get_employee_by_qr(db, qr_code=employee.qr_code)
    if db_employee:
        raise HTTPException(status_code=400, detail="QR code already registered")
    return create_employee(db=db, employee=employee)

@router.put("/{employee_id}", response_model=Employee)
def update_existing_employee(employee_id: int, employee: EmployeeUpdate, db: Session = Depends(get_db)):
    db_employee = update_employee(db, employee_id=employee_id, employee=employee)
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return db_employee

@router.delete("/{employee_id}", response_model=Employee)
def deactivate_employee(employee_id: int, db: Session = Depends(get_db)):
    db_employee = delete_employee(db, employee_id=employee_id)
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return db_employee
