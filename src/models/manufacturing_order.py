from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from .base import Base

class ManufacturingOrder(Base):
    __tablename__ = "manufacturing_orders"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(String, nullable=False)          # ← добавлено
    part_number = Column(String, nullable=False)       # ← добавлено
    status = Column(String, default="planned")
    current_operation_id = Column(String, nullable=True)  # ← добавлено
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())  # ← добавлено
