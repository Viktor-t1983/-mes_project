from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship  # ← Убедитесь, что есть
from src.models.base import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
    name = Column(String, index=True)
    description = Column(String)
    product_name = Column(String, index=True)
    quantity = Column(Integer)
    status = Column(String, default="pending")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Обратная связь
    project = relationship("Project", back_populates="orders")

    def __repr__(self):
        return f"<Order {self.name} - {self.product_name}>"
