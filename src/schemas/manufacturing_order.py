from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class ManufacturingOrderBase(BaseModel):
    order_number: str
    customer_order_id: Optional[str] = None
    product_name: str
    product_code: str
    quantity: int
    planned_start: Optional[datetime] = None
    planned_end: Optional[datetime] = None
    status: str = "planned"
    priority: str = "normal"
    notes: Optional[str] = None

class ManufacturingOrderCreate(ManufacturingOrderBase):
    pass

class ManufacturingOrderUpdate(BaseModel):
    order_number: Optional[str] = None
    customer_order_id: Optional[str] = None
    product_name: Optional[str] = None
    product_code: Optional[str] = None
    quantity: Optional[int] = None
    planned_start: Optional[datetime] = None
    planned_end: Optional[datetime] = None
    actual_start: Optional[datetime] = None
    actual_end: Optional[datetime] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    notes: Optional[str] = None

class ManufacturingOrder(ManufacturingOrderBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    actual_start: Optional[datetime] = None
    actual_end: Optional[datetime] = None
    created_at: datetime
