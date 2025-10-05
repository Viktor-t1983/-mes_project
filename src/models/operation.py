from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
from .base import Base

class Operation(Base):
    __tablename__ = "operations"

    id = Column(Integer, primary_key=True, index=True)
    manufacturing_order_id = Column(Integer, ForeignKey("manufacturing_orders.id"), nullable=False)
    operation_number = Column(Integer)
    name = Column(String)
    description = Column(String)
    planned_duration = Column(Integer)  # в минутах
    actual_duration = Column(Integer)   # в минутах
    status = Column(String, default="pending")  # pending, in_progress, paused, completed, defect
    assigned_employee_id = Column(Integer, ForeignKey("employees.id"), nullable=True)
    started_at = Column(DateTime(timezone=True), nullable=True)      # = actual_start
    completed_at = Column(DateTime(timezone=True), nullable=True)    # = actual_end
    quality_check_passed = Column(Boolean, default=False)
    notes = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    operation_type = Column(String)
    workcenter_id = Column(String)
    machine_id = Column(Integer, ForeignKey("machines.id"), nullable=True)

    # Поля для IIoT и OEE (добавлены вручную)
    pause_duration = Column(Integer, default=0)        # суммарное время пауз в минутах
    pause_events = Column(JSONB, default=[])           # список пауз: [{"start": "...", "end": "...", "reason": "..."}]
    planned_start = Column(DateTime(timezone=True), nullable=True)
    planned_end = Column(DateTime(timezone=True), nullable=True)
