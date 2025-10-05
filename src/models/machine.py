from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.sql import func
from .base import Base

class Machine(Base):
    __tablename__ = "machines"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)              # "Токарный станок 1К62"
    type = Column(String, nullable=False)              # "lathe", "milling", "laser"
    location = Column(String)                          # "Цех 1, Линия A"
    status = Column(String, default="online")          # online, offline, maintenance
    last_heartbeat = Column(DateTime(timezone=True), default=func.now())
    machine_token = Column(String, unique=True)        # для аутентификации станков
    technical_docs = Column(Text)                      # JSON с URL паспортов
