import os

def ensure_create_schemas():
    print("🔧 СОЗДАНИЕ ПРОСТЫХ CREATE СХЕМ")
    print("=" * 50)
    
    # Employee
    if not os.path.exists("src/schemas/employee.py"):
        with open("src/schemas/employee.py", "w") as f:
            f.write('''
from pydantic import BaseModel
from typing import Optional, List

class EmployeeBase(BaseModel):
    first_name: str
    last_name: str
    role: str

class EmployeeCreate(EmployeeBase):
    pass

class Employee(EmployeeBase):
    id: int
    is_active: bool = True

    class Config:
        from_attributes = True
''')
        print("✅ Создана схема Employee")
    
    # Order
    if not os.path.exists("src/schemas/order.py"):
        with open("src/schemas/order.py", "w") as f:
            f.write('''
from pydantic import BaseModel
from typing import Optional

class OrderBase(BaseModel):
    product_name: str
    quantity: int

class OrderCreate(OrderBase):
    pass

class Order(OrderBase):
    id: int
    status: str = "created"

    class Config:
        from_attributes = True
''')
        print("✅ Создана схема Order")
    
    # ManufacturingOrder
    if not os.path.exists("src/schemas/manufacturing_order.py"):
        with open("src/schemas/manufacturing_order.py", "w") as f:
            f.write('''
from pydantic import BaseModel
from typing import Optional

class ManufacturingOrderBase(BaseModel):
    product_name: str
    quantity: int

class ManufacturingOrderCreate(ManufacturingOrderBase):
    pass

class ManufacturingOrder(ManufacturingOrderBase):
    id: int
    status: str = "planned"

    class Config:
        from_attributes = True
''')
        print("✅ Создана схема ManufacturingOrder")
    
    # Operation
    if not os.path.exists("src/schemas/operation.py"):
        with open("src/schemas/operation.py", "w") as f:
            f.write('''
from pydantic import BaseModel
from typing import Optional

class OperationBase(BaseModel):
    name: str
    description: str

class OperationCreate(OperationBase):
    pass

class Operation(OperationBase):
    id: int
    status: str = "pending"

    class Config:
        from_attributes = True
''')
        print("✅ Создана схема Operation")
    
    # DefectReport
    if not os.path.exists("src/schemas/defect_report.py"):
        with open("src/schemas/defect_report.py", "w") as f:
            f.write('''
from pydantic import BaseModel
from typing import Optional

class DefectReportBase(BaseModel):
    defect_type: str
    defect_description: str
    severity: str

class DefectReportCreate(DefectReportBase):
    pass

class DefectReport(DefectReportBase):
    id: int
    status: str = "reported"

    class Config:
        from_attributes = True
''')
        print("✅ Создана схема DefectReport")
    
    # Project
    if not os.path.exists("src/schemas/project.py"):
        with open("src/schemas/project.py", "w") as f:
            f.write('''
from pydantic import BaseModel
from typing import Optional

class ProjectBase(BaseModel):
    name: str
    description: str

class ProjectCreate(ProjectBase):
    pass

class Project(ProjectBase):
    id: int
    status: str = "active"

    class Config:
        from_attributes = True
''')
        print("✅ Создана схема Project")

if __name__ == "__main__":
    ensure_create_schemas()
