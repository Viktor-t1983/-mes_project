from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Numeric
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .base import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    name = Column(String, index=True)
    description = Column(String)
    quantity = Column(Integer, default=1)
    status = Column(String, default="draft")  # draft, planned, in_progress, completed
    priority = Column(String, default="medium")  # low, medium, high, urgent
    deadline = Column(DateTime(timezone=True))
    
    # Автоматические метки времени
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    completed_at = Column(DateTime(timezone=True))
    
    # Связи
    project = relationship("Project", back_populates="orders")

# Добавляем обратную связь в Project
from .project import Project
Project.orders = relationship("Order", back_populates="project", cascade="all, delete-orphan")
