from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
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
