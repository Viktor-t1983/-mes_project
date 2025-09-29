from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.sql import func
from .base import Base

class Operation(Base):
    __tablename__ = "operations"

    id = Column(Integer, primary_key=True, index=True)
    qr_code = Column(String, unique=True, index=True)  # QR для сканирования
    name = Column(String, index=True)
    description = Column(String)
    planned_duration = Column(Integer)  # в минутах
    actual_duration = Column(Integer, nullable=True)
    status = Column(String, default="pending")  # pending, in_progress, paused, completed, defect
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=True)
    start_time = Column(DateTime(timezone=True), nullable=True)
    end_time = Column(DateTime(timezone=True), nullable=True)
    defect_reason = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
