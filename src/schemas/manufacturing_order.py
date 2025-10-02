from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ManufacturingOrderBase(BaseModel):
    product_name: str
    quantity: int
    status: str = "planned"
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

class ManufacturingOrderCreate(ManufacturingOrderBase):
    pass

class ManufacturingOrderUpdate(ManufacturingOrderBase):
    product_name: Optional[str] = None
    quantity: Optional[int] = None
    status: Optional[str] = None

class ManufacturingOrder(ManufacturingOrderBase):
    id: int
    
    class Config:
        from_attributes = True
