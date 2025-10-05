from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from .base import Base

class AuditLog(Base):
    __tablename__ = "audit_log"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=True)           # None для станков
    machine_id = Column(Integer, nullable=True)        # None для пользователей
    action = Column(String, nullable=False)            # "operation_start", "defect_reported"
    ip_address = Column(String)
    timestamp = Column(DateTime(timezone=True), default=func.now())
    data_snapshot = Column(Text)                       # JSON с контекстом
