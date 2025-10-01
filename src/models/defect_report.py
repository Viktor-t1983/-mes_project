from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Numeric
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
