from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import os
import sys
import uuid
from sqlalchemy.exc import IntegrityError
from fastapi.middleware.cors import CORSMiddleware

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.database import get_db, engine, Base
from src.models.employee import Employee
from src.models.manufacturing_order import ManufacturingOrder
from src.models.operation import Operation
from src.models.defect_report import DefectReport
from src.models.order import Order
from src.models.project import Project

# Создаем простые схемы напрямую чтобы избежать проблем с импортом
from pydantic import BaseModel

class EmployeeCreate(BaseModel):
    first_name: str
    last_name: str
    role: str
    qr_code: str = None

class EmployeeSchema(EmployeeCreate):
    id: int
    is_active: bool = True

class OrderCreate(BaseModel):
    name: str = "Default Order"
    description: str = "Default description"
    product_name: str
    quantity: int

class OrderSchema(OrderCreate):
    id: int
    status: str = "created"

class ManufacturingOrderCreate(BaseModel):
    order_number: str = None
    product_name: str
    product_code: str = "PROD-DEFAULT"
    quantity: int

class ManufacturingOrderSchema(ManufacturingOrderCreate):
    id: int
    status: str = "planned"

class OperationCreate(BaseModel):
    manufacturing_order_id: int = 1
    operation_number: str = None
    name: str
    description: str
    planned_duration: int = 60

class OperationSchema(OperationCreate):
    id: int
    status: str = "pending"

class OperationAction(BaseModel):
    operation_id: int

class DefectReportCreate(BaseModel):
    manufacturing_order_id: int = 1
    reported_by: int = 1
    defect_type: str
    defect_description: str
    severity: str

class DefectReportSchema(DefectReportCreate):
    id: int
    status: str = "reported"

class ProjectCreate(BaseModel):
    name: str
    description: str

class ProjectSchema(ProjectCreate):
    id: int
    status: str = "active"

# QR code generator
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

# Добавляем CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def generate_unique_qr_code():
    """Generate unique QR code for employees"""
    return f"EMP-{uuid.uuid4().hex[:8].upper()}"

def generate_unique_order_number():
    """Generate unique order number for manufacturing orders"""
    return f"MO-{uuid.uuid4().hex[:6].upper()}"

def generate_unique_operation_number():
    """Generate unique operation number"""
    return f"OP-{uuid.uuid4().hex[:6].upper()}"

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
    """Get all employees"""
    return db.query(Employee).all()

@app.post("/api/v1/employees", response_model=EmployeeSchema)
def create_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):
    """Create new employee"""
    # Генерируем уникальный QR код если не предоставлен
    qr_code = employee.qr_code or generate_unique_qr_code()
    
    db_employee = Employee(
        first_name=employee.first_name,
        last_name=employee.last_name,
        role=employee.role,
        qr_code=qr_code,
        is_active=True
    )
    
    try:
        db.add(db_employee)
        db.commit()
        db.refresh(db_employee)
        return db_employee
    except IntegrityError:
        db.rollback()
        # Если ошибка из-за дубликата QR кода, генерируем новый
        qr_code = generate_unique_qr_code()
        db_employee.qr_code = qr_code
        db.add(db_employee)
        db.commit()
        db.refresh(db_employee)
        return db_employee
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating employee: {str(e)}")

# ========== ORDER ENDPOINTS ==========
@app.get("/api/v1/orders", response_model=List[OrderSchema])
def get_orders(db: Session = Depends(get_db)):
    """Get all orders"""
    return db.query(Order).all()

@app.post("/api/v1/orders", response_model=OrderSchema)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    """Create new order"""
    db_order = Order(
        name=order.name,
        description=order.description,
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
    """Get all manufacturing orders"""
    return db.query(ManufacturingOrder).all()

@app.post("/api/v1/mo", response_model=ManufacturingOrderSchema)
def create_manufacturing_order(mo: ManufacturingOrderCreate, db: Session = Depends(get_db)):
    """Create new manufacturing order"""
    # Генерируем уникальный order_number если не предоставлен
    order_number = mo.order_number or generate_unique_order_number()
    
    db_mo = ManufacturingOrder(
        order_number=order_number,
        product_name=mo.product_name,
        product_code=mo.product_code,
        quantity=mo.quantity,
        status="planned"
    )
    
    try:
        db.add(db_mo)
        db.commit()
        db.refresh(db_mo)
        return db_mo
    except IntegrityError:
        db.rollback()
        # Если ошибка из-за дубликата order_number, генерируем новый
        order_number = generate_unique_order_number()
        db_mo.order_number = order_number
        db.add(db_mo)
        db.commit()
        db.refresh(db_mo)
        return db_mo
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating manufacturing order: {str(e)}")

# ========== OPERATION ENDPOINTS ==========
@app.get("/api/v1/operations", response_model=List[OperationSchema])
def get_operations(db: Session = Depends(get_db)):
    """Get all operations"""
    return db.query(Operation).all()

@app.post("/api/v1/operations", response_model=OperationSchema)
def create_operation(operation: OperationCreate, db: Session = Depends(get_db)):
    """Create new operation"""
    # Генерируем уникальный operation_number если не предоставлен
    operation_number = operation.operation_number or generate_unique_operation_number()
    
    db_operation = Operation(
        manufacturing_order_id=operation.manufacturing_order_id,
        operation_number=operation_number,
        name=operation.name,
        description=operation.description,
        planned_duration=operation.planned_duration,
        status="pending"
    )
    
    try:
        db.add(db_operation)
        db.commit()
        db.refresh(db_operation)
        return db_operation
    except IntegrityError:
        db.rollback()
        # Если ошибка из-за дубликата operation_number, генерируем новый
        operation_number = generate_unique_operation_number()
        db_operation.operation_number = operation_number
        db.add(db_operation)
        db.commit()
        db.refresh(db_operation)
        return db_operation
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating operation: {str(e)}")

@app.post("/api/v1/operations/start")
def start_operation(action: OperationAction, db: Session = Depends(get_db)):
    """Start operation"""
    operation = db.query(Operation).filter(Operation.id == action.operation_id).first()
    if not operation:
        raise HTTPException(status_code=404, detail="Operation not found")
    operation.status = "in_progress"
    db.commit()
    return {"message": "Operation started", "operation_id": action.operation_id}

@app.post("/api/v1/operations/pause")
def pause_operation(action: OperationAction, db: Session = Depends(get_db)):
    """Pause operation"""
    operation = db.query(Operation).filter(Operation.id == action.operation_id).first()
    if not operation:
        raise HTTPException(status_code=404, detail="Operation not found")
    operation.status = "paused"
    db.commit()
    return {"message": "Operation paused", "operation_id": action.operation_id}

@app.post("/api/v1/operations/complete")
def complete_operation(action: OperationAction, db: Session = Depends(get_db)):
    """Complete operation"""
    operation = db.query(Operation).filter(Operation.id == action.operation_id).first()
    if not operation:
        raise HTTPException(status_code=404, detail="Operation not found")
    operation.status = "completed"
    db.commit()
    return {"message": "Operation completed", "operation_id": action.operation_id}

# ========== DEFECT REPORT ENDPOINTS ==========
@app.get("/api/v1/defects", response_model=List[DefectReportSchema])
def get_defect_reports(db: Session = Depends(get_db)):
    """Get all defect reports"""
    return db.query(DefectReport).all()

@app.post("/api/v1/defects", response_model=DefectReportSchema)
def create_defect_report(defect: DefectReportCreate, db: Session = Depends(get_db)):
    """Create new defect report"""
    db_defect = DefectReport(
        manufacturing_order_id=defect.manufacturing_order_id,
        reported_by=defect.reported_by,
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
    """Get all projects"""
    return db.query(Project).all()

@app.post("/api/v1/projects", response_model=ProjectSchema)
def create_project(project: ProjectCreate, db: Session = Depends(get_db)):
    """Create new project"""
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
    """Generate QR code for order"""
    qr_data = f"ORDER:{order_id}"
    return generate_qr_code(qr_data)

@app.get("/api/v1/qr/employee/{employee_id}")
def get_employee_qr(employee_id: int):
    """Generate QR code for employee"""
    qr_data = f"EMPLOYEE:{employee_id}"
    return generate_qr_code(qr_data)

@app.get("/api/v1/qr/mo/{mo_id}")
def get_mo_qr(mo_id: int):
    """Generate QR code for manufacturing order"""
    qr_data = f"MANUFACTURING_ORDER:{mo_id}"
    return generate_qr_code(qr_data)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
