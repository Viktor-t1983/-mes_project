"""
Скрипт для исправления ошибок валидации Pydantic
Запускать в Терминале 2 пока сервер работает в Терминале 1
"""

import os
import sys

def fix_employee_model():
    """Исправляем модель Employee - поле allowed_workcenters"""
    employee_model_path = "src/models/employee.py"
    
    new_content = '''from sqlalchemy import Column, Integer, String, Boolean, JSON, DateTime
from sqlalchemy.sql import func
from src.database import Base

class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    qr_code = Column(String, unique=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    role = Column(String)
    allowed_workcenters = Column(JSON, default=list)  # Исправлено: default=list вместо None
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<Employee {self.first_name} {self.last_name} - {self.role}>"
'''

    with open(employee_model_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("✅ Модель Employee исправлена")

def fix_employee_schema():
    """Исправляем схему Employee"""
    employee_schema_path = "src/schemas/employee.py"
    
    new_content = '''from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class EmployeeBase(BaseModel):
    qr_code: str
    first_name: str
    last_name: str
    role: str
    allowed_workcenters: List[str] = []  # Гарантируем список по умолчанию
    is_active: bool = True

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: Optional[str] = None
    allowed_workcenters: Optional[List[str]] = None
    is_active: Optional[bool] = None

class Employee(EmployeeBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
'''

    with open(employee_schema_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("✅ Схема Employee исправлена")

def fix_operation_model():
    """Исправляем модель Operation - добавляем недостающие поля"""
    operation_model_path = "src/models/operation.py"
    
    new_content = '''from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from src.database import Base

class Operation(Base):
    __tablename__ = "operations"

    id = Column(Integer, primary_key=True, index=True)
    manufacturing_order_id = Column(Integer, ForeignKey("manufacturing_orders.id"))
    operation_number = Column(String, index=True)
    name = Column(String)
    description = Column(String)
    operation_type = Column(String, default="production")  # Добавлено недостающее поле
    workcenter_id = Column(Integer, default=1)  # Добавлено недостающее поле
    planned_duration = Column(Float)
    actual_duration = Column(Float)
    status = Column(String, default="pending")
    assigned_employee_id = Column(Integer, ForeignKey("employees.id"))
    started_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
    quality_check_passed = Column(Boolean)
    notes = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<Operation {self.operation_number} - {self.name}>"
'''

    with open(operation_model_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("✅ Модель Operation исправлена")

def fix_operation_schema():
    """Исправляем схему Operation"""
    operation_schema_path = "src/schemas/operation.py"
    
    new_content = '''from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class OperationBase(BaseModel):
    manufacturing_order_id: int
    operation_number: str
    name: str
    description: str
    operation_type: str = "production"  # Добавлено
    workcenter_id: int = 1  # Добавлено
    planned_duration: float
    actual_duration: Optional[float] = None
    status: str = "pending"
    assigned_employee_id: Optional[int] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    quality_check_passed: Optional[bool] = None
    notes: Optional[str] = None

class OperationCreate(OperationBase):
    pass

class OperationUpdate(BaseModel):
    operation_number: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    operation_type: Optional[str] = None
    workcenter_id: Optional[int] = None
    planned_duration: Optional[float] = None
    actual_duration: Optional[float] = None
    status: Optional[str] = None
    assigned_employee_id: Optional[int] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    quality_check_passed: Optional[bool] = None
    notes: Optional[str] = None

class Operation(OperationBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
'''

    with open(operation_schema_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("✅ Схема Operation исправлена")

def fix_order_model():
    """Исправляем модель Order - добавляем недостающие поля"""
    order_model_path = "src/models/order.py"
    
    new_content = '''from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from src.database import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), default=1)  # Добавлено
    name = Column(String, index=True)  # Добавлено
    description = Column(String)  # Добавлено
    product_name = Column(String, index=True)
    quantity = Column(Integer)
    status = Column(String, default="pending")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<Order {self.name} - {self.product_name}>"
'''

    with open(order_model_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("✅ Модель Order исправлена")

def fix_order_schema():
    """Исправляем схему Order"""
    order_schema_path = "src/schemas/order.py"
    
    new_content = '''from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class OrderBase(BaseModel):
    project_id: int = 1  # Добавлено
    name: str  # Добавлено
    description: str  # Добавлено
    product_name: str
    quantity: int
    status: str = "pending"

class OrderCreate(OrderBase):
    pass

class OrderUpdate(BaseModel):
    project_id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    product_name: Optional[str] = None
    quantity: Optional[int] = None
    status: Optional[str] = None

class Order(OrderBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
'''

    with open(order_schema_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("✅ Схема Order исправлена")

def fix_project_model():
    """Исправляем модель Project - добавляем поле status"""
    project_model_path = "src/models/project.py"
    
    new_content = '''from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from src.database import Base

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    status = Column(String, default="active")  # Добавлено недостающее поле
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<Project {self.name}>"
'''

    with open(project_model_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("✅ Модель Project исправлена")

def fix_project_schema():
    """Исправляем схему Project"""
    project_schema_path = "src/schemas/project.py"
    
    new_content = '''from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ProjectBase(BaseModel):
    name: str
    description: str
    status: str = "active"  # Добавлено

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None

class Project(ProjectBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
'''

    with open(project_schema_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("✅ Схема Project исправлена")

def main():
    print("🛠 ИСПРАВЛЕНИЕ ОШИБОК ВАЛИДАЦИИ PYDANTIC")
    print("=" * 50)
    
    # Исправляем все модели и схемы
    fix_employee_model()
    fix_employee_schema()
    fix_operation_model()
    fix_operation_schema()
    fix_order_model()
    fix_order_schema()
    fix_project_model()
    fix_project_schema()
    
    print("\\n✅ ВСЕ ИСПРАВЛЕНИЯ ЗАВЕРШЕНЫ!")
    print("Сервер автоматически перезагрузится благодаря --reload")
    print("Проверьте эндпоинты через: http://localhost:8000/docs")

if __name__ == "__main__":
    main()
