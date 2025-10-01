"""
Создаем минимальные модели без отношений для тестирования
"""

def create_minimal_operation():
    content = '''from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from sqlalchemy.sql import func
from src.core.database import Base

class Operation(Base):
    __tablename__ = "operations"

    id = Column(Integer, primary_key=True, index=True)
    manufacturing_order_id = Column(Integer)
    operation_number = Column(String, index=True)
    name = Column(String)
    description = Column(String)
    operation_type = Column(String, default="production")
    workcenter_id = Column(Integer, default=1)
    planned_duration = Column(Float)
    actual_duration = Column(Float)
    status = Column(String, default="pending")
    assigned_employee_id = Column(Integer)
    started_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
    quality_check_passed = Column(Boolean)
    notes = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<Operation {self.operation_number} - {self.name}>"
'''

    with open("src/models/operation.py", "w", encoding="utf-8") as f:
        f.write(content)
    print("✅ Создана минимальная Operation модель")

def create_minimal_manufacturing_order():
    content = '''from sqlalchemy import Column, Integer, String, DateTime, Text, Numeric
from sqlalchemy.sql import func
from src.core.database import Base

class ManufacturingOrder(Base):
    __tablename__ = "manufacturing_orders"

    id = Column(Integer, primary_key=True, index=True)
    order_number = Column(String(50), unique=True, index=True, nullable=False)
    customer_order_id = Column(Integer)
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
        f.write(content)
    print("✅ Создана минимальная ManufacturingOrder модель")

if __name__ == "__main__":
    print("🛠 СОЗДАНИЕ МИНИМАЛЬНЫХ МОДЕЛЕЙ")
    create_minimal_operation()
    create_minimal_manufacturing_order()
    print("\n✅ МИНИМАЛЬНЫЕ МОДЕЛИ СОЗДАНЫ!")
