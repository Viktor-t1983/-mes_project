"""
Удаляем проблемные отношения чтобы избежать ошибок конфигурации
"""

def remove_relationships_from_operation():
    """Удаляем отношения из Operation модели"""
    operation_content = '''from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from src.core.database import Base

class Operation(Base):
    __tablename__ = "operations"

    id = Column(Integer, primary_key=True, index=True)
    manufacturing_order_id = Column(Integer, ForeignKey("manufacturing_orders.id"))
    operation_number = Column(String, index=True)
    name = Column(String)
    description = Column(String)
    operation_type = Column(String, default="production")
    workcenter_id = Column(Integer, default=1)
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

    with open("src/models/operation.py", "w", encoding="utf-8") as f:
        f.write(operation_content)
    print("✅ Удалены отношения из Operation модели")

def remove_relationships_from_manufacturing_order():
    """Удаляем отношения из ManufacturingOrder модели"""
    mo_content = '''from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Numeric
from sqlalchemy.sql import func
from src.core.database import Base

class ManufacturingOrder(Base):
    __tablename__ = "manufacturing_orders"

    id = Column(Integer, primary_key=True, index=True)
    order_number = Column(String(50), unique=True, index=True, nullable=False)
    customer_order_id = Column(Integer, ForeignKey("orders.id"))
    product_name = Column(String(100), nullable=False)
    product_code = Column(String(50))
    quantity = Column(Integer, nullable=False)
    planned_start = Column(DateTime(timezone=True))
    planned_end = Column(DateTime(timezone=True))
    actual_start = Column(DateTime(timezone=True))
    actual_end = Column(DateTime(timezone=True))
    status = Column(String(20), default="planned")
    priority = Column(String(20), default="medium")
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<ManufacturingOrder {self.order_number}>"
'''

    with open("src/models/manufacturing_order.py", "w", encoding="utf-8") as f:
        f.write(mo_content)
    print("✅ Удалены отношения из ManufacturingOrder модели")

def remove_relationships_from_defect_report():
    """Удаляем отношения из DefectReport модели"""
    defect_content = '''from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Numeric
from sqlalchemy.sql import func
from src.core.database import Base

class DefectReport(Base):
    __tablename__ = "defect_reports"

    id = Column(Integer, primary_key=True, index=True)
    manufacturing_order_id = Column(Integer, ForeignKey("manufacturing_orders.id"))
    operation_id = Column(Integer, ForeignKey("operations.id"))
    reported_by = Column(Integer, ForeignKey("employees.id"))
    defect_type = Column(String(100))
    defect_description = Column(Text)
    severity = Column(String(20))
    quantity_affected = Column(Integer)
    corrective_action = Column(Text)
    status = Column(String(20), default="open")
    resolved_at = Column(DateTime(timezone=True))
    resolved_by = Column(Integer, ForeignKey("employees.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<DefectReport {self.id} - {self.defect_type}>"
'''

    with open("src/models/defect_report.py", "w", encoding="utf-8") as f:
        f.write(defect_content)
    print("✅ Удалены отношения из DefectReport модели")

def simplify_employee_model():
    """Упрощаем Employee модель"""
    employee_content = '''from sqlalchemy import Column, Integer, String, Boolean, JSON, DateTime
from sqlalchemy.sql import func
from src.core.database import Base

class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    qr_code = Column(String, unique=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    role = Column(String)
    allowed_workcenters = Column(JSON, default=list)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<Employee {self.first_name} {self.last_name} - {self.role}>"
'''

    with open("src/models/employee.py", "w", encoding="utf-8") as f:
        f.write(employee_content)
    print("✅ Упрощена Employee модель")

if __name__ == "__main__":
    print("🛠 УДАЛЕНИЕ ПРОБЛЕМНЫХ ОТНОШЕНИЙ")
    remove_relationships_from_operation()
    remove_relationships_from_manufacturing_order()
    remove_relationships_from_defect_report()
    simplify_employee_model()
    print("\n✅ ВСЕ ОТНОШЕНИЯ ИСПРАВЛЕНЫ!")
