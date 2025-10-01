import os

def fix_all_schemas():
    print("🔧 ИСПРАВЛЕНИЕ ВСЕХ СХЕМ CREATE")
    print("=" * 50)
    
    # Employee схема - добавляем qr_code как опциональное поле
    employee_schema = '''
from pydantic import BaseModel
from typing import Optional

class EmployeeBase(BaseModel):
    first_name: str
    last_name: str
    role: str
    qr_code: Optional[str] = None

class EmployeeCreate(EmployeeBase):
    pass

class Employee(EmployeeBase):
    id: int
    is_active: bool = True

    class Config:
        from_attributes = True
'''
    
    with open("src/schemas/employee.py", "w") as f:
        f.write(employee_schema)
    print("✅ Исправлена схема Employee")
    
    # Order схема - добавляем name и description
    order_schema = '''
from pydantic import BaseModel
from typing import Optional

class OrderBase(BaseModel):
    name: str
    description: str
    product_name: str
    quantity: int

class OrderCreate(OrderBase):
    pass

class Order(OrderBase):
    id: int
    status: str = "created"

    class Config:
        from_attributes = True
'''
    
    with open("src/schemas/order.py", "w") as f:
        f.write(order_schema)
    print("✅ Исправлена схема Order")
    
    # ManufacturingOrder схема - добавляем order_number и product_code
    manufacturing_order_schema = '''
from pydantic import BaseModel
from typing import Optional

class ManufacturingOrderBase(BaseModel):
    order_number: str
    product_name: str
    product_code: str
    quantity: int

class ManufacturingOrderCreate(ManufacturingOrderBase):
    pass

class ManufacturingOrder(ManufacturingOrderBase):
    id: int
    status: str = "planned"

    class Config:
        from_attributes = True
'''
    
    with open("src/schemas/manufacturing_order.py", "w") as f:
        f.write(manufacturing_order_schema)
    print("✅ Исправлена схема ManufacturingOrder")
    
    # Operation схема - добавляем обязательные поля
    operation_schema = '''
from pydantic import BaseModel
from typing import Optional

class OperationBase(BaseModel):
    manufacturing_order_id: int
    operation_number: str
    name: str
    description: str
    planned_duration: int

class OperationCreate(OperationBase):
    pass

class Operation(OperationBase):
    id: int
    status: str = "pending"

    class Config:
        from_attributes = True
'''
    
    with open("src/schemas/operation.py", "w") as f:
        f.write(operation_schema)
    print("✅ Исправлена схема Operation")
    
    # DefectReport схема - добавляем обязательные поля
    defect_report_schema = '''
from pydantic import BaseModel
from typing import Optional

class DefectReportBase(BaseModel):
    manufacturing_order_id: int
    reported_by: int
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
'''
    
    with open("src/schemas/defect_report.py", "w") as f:
        f.write(defect_report_schema)
    print("✅ Исправлена схема DefectReport")
    
    # Project схема - оставляем как есть (работает)
    project_schema = '''
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
'''
    
    with open("src/schemas/project.py", "w") as f:
        f.write(project_schema)
    print("✅ Обновлена схема Project")

if __name__ == "__main__":
    fix_all_schemas()
