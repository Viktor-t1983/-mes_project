from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from src.models.base import Base

class Operation(Base):
    __tablename__ = "operations"
    id = Column(Integer, primary_key=True, index=True)
    employee_qr = Column(String, index=True)
    part_number = Column(String, index=True)
    workcenter_id = Column(String, index=True)
    status = Column(String, default="created")  # created → started → paused → completed
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
