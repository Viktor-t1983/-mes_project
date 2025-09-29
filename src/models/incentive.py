from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Numeric
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from . import Base

class Incentive(Base):
    __tablename__ = "incentives"
    
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    period = Column(String(7), nullable=False)
    calculation_date = Column(DateTime(timezone=True), server_default=func.now())
    
    completed_operations = Column(Integer, default=0)
    quality_score = Column(Numeric(5, 2), default=0)
    efficiency_score = Column(Numeric(5, 2), default=0)
    defect_count = Column(Integer, default=0)
    overtime_hours = Column(Numeric(8, 2), default=0)
    
    base_amount = Column(Numeric(12, 2), default=0)
    quality_bonus = Column(Numeric(12, 2), default=0)
    efficiency_bonus = Column(Numeric(12, 2), default=0)
    defect_penalty = Column(Numeric(12, 2), default=0)
    total_amount = Column(Numeric(12, 2), default=0)
    
    status = Column(String(20), default="calculated")
    paid_at = Column(DateTime(timezone=True))
    notes = Column(Text)
    
    def __repr__(self):
        return f"<Incentive {self.employee_id} - {self.period} - {self.total_amount}>"
