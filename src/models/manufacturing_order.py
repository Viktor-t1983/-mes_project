from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Numeric
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from . import Base

class ManufacturingOrder(Base):
    __tablename__ = "manufacturing_orders"
    
    id = Column(Integer, primary_key=True, index=True)
    order_number = Column(String(50), unique=True, index=True, nullable=False)
    customer_order_id = Column(String(100))
    product_name = Column(String(200), nullable=False)
    product_code = Column(String(100), nullable=False)
    quantity = Column(Integer, nullable=False)
    planned_start = Column(DateTime(timezone=True))
    planned_end = Column(DateTime(timezone=True))
    actual_start = Column(DateTime(timezone=True))
    actual_end = Column(DateTime(timezone=True))
    status = Column(String(50), default="planned")
    priority = Column(String(20), default="normal")
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    operations = relationship("Operation", back_populates="manufacturing_order")
    defect_reports = relationship("DefectReport", back_populates="manufacturing_order")
    
    def __repr__(self):
        return f"<ManufacturingOrder {self.order_number} - {self.product_name}>"
