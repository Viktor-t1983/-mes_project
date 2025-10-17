from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.sql import func
from src.models.base import Base

class OfflineEvent(Base):
    __tablename__ = "offline_events"
    id = Column(Integer, primary_key=True)
    employee_qr = Column(String, index=True)
    event_type = Column(String)  # "start", "pause", "complete"
    payload = Column(Text)       # JSON с данными операции
    is_synced = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
