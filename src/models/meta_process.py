from sqlalchemy import Column, Integer, String, JSON, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from src.models.base import Base
from datetime import datetime

class MetaProcess(Base):
    __tablename__ = "meta_processes"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String)
    version = Column(String, default="1.0")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    steps = relationship("MetaStep", back_populates="process", cascade="all, delete-orphan")

class MetaStep(Base):
    __tablename__ = "meta_steps"
    id = Column(Integer, primary_key=True, index=True)
    process_id = Column(Integer, ForeignKey("meta_processes.id"), nullable=False)
    step_order = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
    action_type = Column(String, nullable=False)  # "form", "approval", "notification", "integration"
    config = Column(JSON, nullable=False)  # schema, roles, conditions, etc.
    process = relationship("MetaProcess", back_populates="steps")
