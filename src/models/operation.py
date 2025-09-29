from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Numeric, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from . import Base

class Operation(Base):
    __tablename__ = "operations"
    
    id = Column(Integer, primary_key=True, index=True)
    manufacturing_order_id = Column(Integer, ForeignKey("manufacturing_orders.id"), nullable=False)
    operation_number = Column(String(50), nullable=False)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    planned_duration = Column(Numeric(10, 2))
    actual_duration = Column(Numeric(10, 2))
    status = Column(String(50), default="pending")
    assigned_employee_id = Column(Integer, ForeignKey("employees.id"))
    started_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
    quality_check_passed = Column(Boolean)
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    manufacturing_order = relationship("ManufacturingOrder", back_populates="operations")
    defect_reports = relationship("DefectReport", back_populates="operation")
    
    def __repr__(self):
        return f"<Operation {self.operation_number} - {self.name}>"
