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

# Импортируем схемы напрямую чтобы избежать проблем с __init__.py
try:
    from src.schemas.employee import Employee as EmployeeSchema, EmployeeCreate
except ImportError:
    # Создаем простые схемы на лету если импорт не работает
    from pydantic import BaseModel
    class EmployeeCreate(BaseModel):
        first_name: str
        last_name: str
        role: str
        qr_code: str = None
    class EmployeeSchema(EmployeeCreate):
        id: int
        is_active: bool = True

try:
    from src.schemas.manufacturing_order import ManufacturingOrder as ManufacturingOrderSchema, ManufacturingOrderCreate
except ImportError:
    from pydantic import BaseModel
    class ManufacturingOrderCreate(BaseModel):
        order_number: str = "MO-DEFAULT"
        product_name: str
        product_code: str = "PROD-DEFAULT"
        quantity: int
    class ManufacturingOrderSchema(ManufacturingOrderCreate):
        id: int
        status: str = "planned"

try:
    from src.schemas.operation import Operation as OperationSchema, OperationCreate
except ImportError:
    from pydantic import BaseModel
    class OperationCreate(BaseModel):
        manufacturing_order_id: int = 1
        operation_number: str = "OP-DEFAULT"
        name: str
        description: str
        planned_duration: int = 60
    class OperationSchema(OperationCreate):
        id: int
        status: str = "pending"

try:
    from src.schemas.defect_report import DefectReport as DefectReportSchema, DefectReportCreate
except ImportError:
    from pydantic import BaseModel
    class DefectReportCreate(BaseModel):
        manufacturing_order_id: int = 1
        reported_by: int = 1
        defect_type: str
        defect_description: str
        severity: str
    class DefectReportSchema(DefectReportCreate):
        id: int
        status: str = "reported"

try:
    from src.schemas.order import Order as OrderSchema, OrderCreate
except ImportError:
    from pydantic import BaseModel
    class OrderCreate(BaseModel):
        name: str = "Default Order"
        description: str = "Default description"
        product_name: str
        quantity: int
    class OrderSchema(OrderCreate):
        id: int
        status: str = "created"

try:
    from src.schemas.project import Project as ProjectSchema, ProjectCreate
except ImportError:
    from pydantic import BaseModel
    class ProjectCreate(BaseModel):
        name: str
        description: str
    class ProjectSchema(ProjectCreate):
        id: int
        status: str = "active"

try:
    from src.utils.qrcode_generator import generate_qr_code
except ImportError:
    def generate_qr_code(data: str):
        from fastapi.responses import Response
        import qrcode
        from io import BytesIO
        qr = qrcode.QRCode(version=1, box_size=10, border=4)
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img_buffer = BytesIO()
        img.save(img_buffer, format="PNG")
        img_buffer.seek(0)
        return Response(content=img_buffer.getvalue(), media_type="image/png")

Base.metadata.create_all(bind=engine)

app = FastAPI(title="MES System", version="1.0.0")

# ========== ROOT & HEALTH ==========
@app.get("/")
async def root():
    return {"message": "MES System API"}

@app.get("/api/v1/health")
async def health_check():
    return {"status": "healthy", "message": "MES System is running"}

# ========== EMPLOYEE ENDPOINTS ==========
@app.get("/api/v1/employees", response_model=List[EmployeeSchema])
def get_employees(db: Session = Depends(get_db)):
    return db.query(Employee).all()

@app.post("/api/v1/employees", response_model=EmployeeSchema)
def create_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):
    db_employee = Employee(
        first_name=employee.first_name,
        last_name=employee.last_name,
        role=employee.role,
        qr_code=getattr(employee, 'qr_code', None),
        is_active=True
    )
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee

# ========== ORDER ENDPOINTS ==========
@app.get("/api/v1/orders", response_model=List[OrderSchema])
def get_orders(db: Session = Depends(get_db)):
    return db.query(Order).all()

@app.post("/api/v1/orders", response_model=OrderSchema)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    db_order = Order(
        name=getattr(order, 'name', order.product_name),
        description=getattr(order, 'description', ''),
        product_name=order.product_name,
        quantity=order.quantity,
        status="created"
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

# ========== MANUFACTURING ORDER ENDPOINTS ==========
@app.get("/api/v1/mo", response_model=List[ManufacturingOrderSchema])
def get_manufacturing_orders(db: Session = Depends(get_db)):
    return db.query(ManufacturingOrder).all()

@app.post("/api/v1/mo", response_model=ManufacturingOrderSchema)
def create_manufacturing_order(mo: ManufacturingOrderCreate, db: Session = Depends(get_db)):
    db_mo = ManufacturingOrder(
        order_number=getattr(mo, 'order_number', 'MO-' + str(hash(mo.product_name))[-6:]),
        product_name=mo.product_name,
        product_code=getattr(mo, 'product_code', 'PROD-' + str(hash(mo.product_name))[-6:]),
        quantity=mo.quantity,
        status="planned"
    )
    db.add(db_mo)
    db.commit()
    db.refresh(db_mo)
    return db_mo

# ========== OPERATION ENDPOINTS ==========
@app.get("/api/v1/operations", response_model=List[OperationSchema])
def get_operations(db: Session = Depends(get_db)):
    return db.query(Operation).all()

@app.post("/api/v1/operations", response_model=OperationSchema)
def create_operation(operation: OperationCreate, db: Session = Depends(get_db)):
    db_operation = Operation(
        manufacturing_order_id=getattr(operation, 'manufacturing_order_id', 1),
        operation_number=getattr(operation, 'operation_number', 'OP-' + str(hash(operation.name))[-6:]),
        name=operation.name,
        description=operation.description,
        planned_duration=getattr(operation, 'planned_duration', 60),
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

# ========== DEFECT REPORT ENDPOINTS ==========
@app.get("/api/v1/defects", response_model=List[DefectReportSchema])
def get_defect_reports(db: Session = Depends(get_db)):
    return db.query(DefectReport).all()

@app.post("/api/v1/defects", response_model=DefectReportSchema)
def create_defect_report(defect: DefectReportCreate, db: Session = Depends(get_db)):
    db_defect = DefectReport(
        manufacturing_order_id=getattr(defect, 'manufacturing_order_id', 1),
        reported_by=getattr(defect, 'reported_by', 1),
        defect_type=defect.defect_type,
        defect_description=defect.defect_description,
        severity=defect.severity,
        status="reported"
    )
    db.add(db_defect)
    db.commit()
    db.refresh(db_defect)
    return db_defect

# ========== PROJECT ENDPOINTS ==========
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

# ========== QR CODE ENDPOINTS ==========
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
