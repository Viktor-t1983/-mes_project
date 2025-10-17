from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from src.models.base import Base

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    product_name = Column(String, index=True)
    quantity = Column(Integer)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    status = Column(String, default="created")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Связь с Project
    project = relationship("Project", back_populates="orders")
