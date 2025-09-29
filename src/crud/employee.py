from sqlalchemy.orm import Session
from sqlalchemy import and_
from src.models.employee import Employee
from src.schemas.employee import EmployeeCreate, EmployeeUpdate

def get_employee(db: Session, employee_id: int):
    return db.query(Employee).filter(Employee.id == employee_id).first()

def get_employee_by_qr(db: Session, qr_code: str):
    return db.query(Employee).filter(Employee.qr_code == qr_code).first()

def get_employees(db: Session, skip: int = 0, limit: int = 100, active_only: bool = True):
    query = db.query(Employee)
    if active_only:
        query = query.filter(Employee.is_active == True)
    return query.offset(skip).limit(limit).all()

def create_employee(db: Session, employee: EmployeeCreate):
    db_employee = Employee(
        qr_code=employee.qr_code,
        first_name=employee.first_name,
        last_name=employee.last_name,
        position=employee.position,
        department=employee.department,
        qualifications=employee.qualifications,
        is_active=employee.is_active
    )
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee

def update_employee(db: Session, employee_id: int, employee: EmployeeUpdate):
    db_employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if db_employee:
        update_data = employee.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_employee, field, value)
        db.commit()
        db.refresh(db_employee)
    return db_employee

def delete_employee(db: Session, employee_id: int):
    db_employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if db_employee:
        db_employee.is_active = False
        db.commit()
        db.refresh(db_employee)
    return db_employee
