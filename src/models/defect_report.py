from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Numeric
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from . import Base

class DefectReport(Base):
    __tablename__ = "defect_reports"
    
    id = Column(Integer, primary_key=True, index=True)
    manufacturing_order_id = Column(Integer, ForeignKey("manufacturing_orders.id"), nullable=False)
    operation_id = Column(Integer, ForeignKey("operations.id"))
    reported_by = Column(Integer, ForeignKey("employees.id"), nullable=False)
    defect_type = Column(String(100), nullable=False)
    defect_description = Column(Text, nullable=False)
    severity = Column(String(20), default="medium")
    quantity_affected = Column(Integer, default=1)
    corrective_action = Column(Text)
    status = Column(String(50), default="reported")
    resolved_at = Column(DateTime(timezone=True))
    resolved_by = Column(Integer, ForeignKey("employees.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    manufacturing_order = relationship("ManufacturingOrder", back_populates="defect_reports")
    operation = relationship("Operation", back_populates="defect_reports")
    
    def __repr__(self):
        return f"<DefectReport {self.defect_type} - {self.severity}>"
