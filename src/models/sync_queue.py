from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from sqlalchemy.sql import func
from src.models.base import Base

class SyncQueue(Base):
    __tablename__ = "sync_queue"
    id = Column(Integer, primary_key=True, index=True)
    entity_type = Column(String, nullable=False)  # "shipment", "order"
    entity_id = Column(Integer, nullable=False)
    payload = Column(Text, nullable=False)  # JSON
    is_synced = Column(Boolean, default=False)
    error_count = Column(Integer, default=0)
    last_error = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
