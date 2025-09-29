from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Numeric, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from . import Base

class WarehouseItem(Base):
    __tablename__ = "warehouse_items"
    
    id = Column(Integer, primary_key=True, index=True)
    item_code = Column(String(100), unique=True, index=True, nullable=False)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    category = Column(String(100), nullable=False)
    unit = Column(String(50), nullable=False)
    current_quantity = Column(Numeric(15, 3), default=0)
    min_quantity = Column(Numeric(15, 3), default=0)
    max_quantity = Column(Numeric(15, 3))
    location = Column(String(100))
    supplier = Column(String(200))
    is_active = Column(Boolean, default=True)
    last_restocked = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<WarehouseItem {self.item_code} - {self.name} ({self.current_quantity} {self.unit})>"
