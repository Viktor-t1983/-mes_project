from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.database import get_db, engine, Base
from src.models.employee import Employee
from src.models.manufacturing_order import ManufacturingOrder
from src.models.operation import Operation
from src.models.defect_report import DefectReport
from src.models.order import Order
from src.models.project import Project

from src.schemas.employee import Employee as EmployeeSchema, EmployeeCreate
from src.schemas.manufacturing_order import ManufacturingOrder as ManufacturingOrderSchema, ManufacturingOrderCreate
from src.schemas.operation import Operation as OperationSchema, OperationCreate
from src.schemas.defect_report import DefectReport as DefectReportSchema, DefectReportCreate
from src.schemas.order import Order as OrderSchema, OrderCreate
from src.schemas.project import Project as ProjectSchema, ProjectCreate

from src.utils.qrcode_generator import generate_qr_code

Base.metadata.create_all(bind=engine)

app = FastAPI(title="MES System", version="1.0.0")

@app.get("/api/v1/health")
async def health_check():
    return {"status": "healthy", "message": "MES System is running"}

# EMPLOYEE ENDPOINTS
@app.get("/api/v1/employees", response_model=List[EmployeeSchema])
def get_employees(db: Session = Depends(get_db)):
    return db.query(Employee).all()

@app.post("/api/v1/employees", response_model=EmployeeSchema)
def create_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):
    db_employee = Employee(
        first_name=employee.first_name,
        last_name=employee.last_name,
        role=employee.role,
        is_active=True
    )
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee

# ORDER ENDPOINTS
@app.get("/api/v1/orders", response_model=List[OrderSchema])
def get_orders(db: Session = Depends(get_db)):
    return db.query(Order).all()

@app.post("/api/v1/orders", response_model=OrderSchema)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    db_order = Order(
        product_name=order.product_name,
        quantity=order.quantity,
        status="created"
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

# MANUFACTURING ORDER ENDPOINTS
@app.get("/api/v1/mo", response_model=List[ManufacturingOrderSchema])
def get_manufacturing_orders(db: Session = Depends(get_db)):
    return db.query(ManufacturingOrder).all()

@app.post("/api/v1/mo", response_model=ManufacturingOrderSchema)
def create_manufacturing_order(mo: ManufacturingOrderCreate, db: Session = Depends(get_db)):
    db_mo = ManufacturingOrder(
        product_name=mo.product_name,
        quantity=mo.quantity,
        status="planned"
    )
    db.add(db_mo)
    db.commit()
    db.refresh(db_mo)
    return db_mo

# OPERATION ENDPOINTS
@app.get("/api/v1/operations", response_model=List[OperationSchema])
def get_operations(db: Session = Depends(get_db)):
    return db.query(Operation).all()

@app.post("/api/v1/operations", response_model=OperationSchema)
def create_operation(operation: OperationCreate, db: Session = Depends(get_db)):
    db_operation = Operation(
        name=operation.name,
        description=operation.description,
        status="pending"
    )
    db.add(db_operation)
    db.commit()
    db.refresh(db_operation)
    return db_operation

@app.post("/api/v1/operations/start")
def start_operation(operation_id: int, db: Session = Depends(get_db)):
    operation = db.query(Operation).filter(Operation.id == operation_id).first()
    if not operation:
        raise HTTPException(status_code=404, detail="Operation not found")
    operation.status = "in_progress"
    db.commit()
    return {"message": "Operation started", "operation_id": operation_id}

@app.post("/api/v1/operations/pause")
def pause_operation(operation_id: int, db: Session = Depends(get_db)):
    operation = db.query(Operation).filter(Operation.id == operation_id).first()
    if not operation:
        raise HTTPException(status_code=404, detail="Operation not found")
    operation.status = "paused"
    db.commit()
    return {"message": "Operation paused", "operation_id": operation_id}

@app.post("/api/v1/operations/complete")
def complete_operation(operation_id: int, db: Session = Depends(get_db)):
    operation = db.query(Operation).filter(Operation.id == operation_id).first()
    if not operation:
        raise HTTPException(status_code=404, detail="Operation not found")
    operation.status = "completed"
    db.commit()
    return {"message": "Operation completed", "operation_id": operation_id}

# DEFECT REPORT ENDPOINTS
@app.get("/api/v1/defects", response_model=List[DefectReportSchema])
def get_defect_reports(db: Session = Depends(get_db)):
    return db.query(DefectReport).all()

@app.post("/api/v1/defects", response_model=DefectReportSchema)
def create_defect_report(defect: DefectReportCreate, db: Session = Depends(get_db)):
    db_defect = DefectReport(
        defect_type=defect.defect_type,
        defect_description=defect.defect_description,
        severity=defect.severity,
        status="reported"
    )
    db.add(db_defect)
    db.commit()
    db.refresh(db_defect)
    return db_defect

# PROJECT ENDPOINTS
@app.get("/api/v1/projects", response_model=List[ProjectSchema])
def get_projects(db: Session = Depends(get_db)):
    return db.query(Project).all()

@app.post("/api/v1/projects", response_model=ProjectSchema)
def create_project(project: ProjectCreate, db: Session = Depends(get_db)):
    db_project = Project(
        name=project.name,
        description=project.description,
        status="active"
    )
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

# QR CODE ENDPOINTS
@app.get("/api/v1/qr/order/{order_id}")
def get_order_qr(order_id: int):
    qr_data = f"ORDER:{order_id}"
    return generate_qr_code(qr_data)

@app.get("/api/v1/qr/employee/{employee_id}")
def get_employee_qr(employee_id: int):
    qr_data = f"EMPLOYEE:{employee_id}"
    return generate_qr_code(qr_data)

@app.get("/api/v1/qr/mo/{mo_id}")
def get_mo_qr(mo_id: int):
    qr_data = f"MANUFACTURING_ORDER:{mo_id}"
    return generate_qr_code(qr_data)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
